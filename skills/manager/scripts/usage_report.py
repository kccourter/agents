#!/usr/bin/env python3
"""Export bounded, explicitly selected per-response rollout usage (stdlib only)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

from task_record import invalid_constant, load_record, resolve_path, unique_object

COUNTERS = ('input_tokens', 'cached_input_tokens', 'output_tokens',
            'reasoning_output_tokens', 'cache_write_input_tokens')


def iso(value):
    if not isinstance(value, str):
        raise ValueError('timestamp must be an ISO string')
    stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if stamp.tzinfo is None:
        raise ValueError('timestamp must include timezone')
    return stamp


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, name):
    if not isinstance(value, list) or not all(nonempty(x) for x in value):
        raise ValueError(f'{name} must be a list of nonempty strings')
    return value


def totals():
    return dict.fromkeys((*COUNTERS, 'uncached_input_tokens', 'total_tokens', 'responses'), 0)


def add(target, usage):
    for key in COUNTERS:
        # An omitted optional cache-write counter cannot be reported as known zero.
        if target[key] is None or usage[key] is None:
            target[key] = None
        else:
            target[key] += usage[key]
    target['uncached_input_tokens'] += usage['input_tokens'] - usage['cached_input_tokens']
    target['total_tokens'] += usage['input_tokens'] + usage['output_tokens']
    target['responses'] += 1


def counters(value):
    if not isinstance(value, dict):
        raise ValueError('missing per-response usage')
    result = {}
    for key in COUNTERS:
        number = value.get(key)
        if key == 'cache_write_input_tokens' and key not in value:
            result[key] = None
            continue
        if type(number) is not int or number < 0:
            raise ValueError(f'invalid {key}')
        result[key] = number
    if result['cached_input_tokens'] > result['input_tokens']:
        raise ValueError('cached input exceeds input')
    if result['reasoning_output_tokens'] > result['output_tokens']:
        raise ValueError('reasoning exceeds output')
    if 'total_tokens' in value:
        n = value['total_tokens']
        if type(n) is not int or n != result['input_tokens'] + result['output_tokens']:
            raise ValueError('invalid total_tokens')
    return result


def report(record):
    state, base = load_record(record)
    cfg = state.get('usage', {})
    roots = strings(cfg.get('root_turn_ids'), 'root_turn_ids')
    if not roots or len(roots) != len(set(roots)):
        raise ValueError('root_turn_ids must be nonempty and unique')
    if not nonempty(cfg.get('scope')):
        raise ValueError('usage.scope must be nonempty')
    specs = cfg.get('sources')
    if not isinstance(specs, list) or not specs:
        raise ValueError('usage.sources must be a nonempty list')
    outcome = cfg.get('outcome')
    if not isinstance(outcome, dict):
        raise ValueError('usage.outcome must be an object')
    json.dumps(outcome, allow_nan=False)
    if outcome.get('status') is not None and not nonempty(outcome['status']):
        raise ValueError('outcome.status must be nonempty or null')
    refs = strings(outcome.get('acceptance_refs', []), 'acceptance_refs')
    elapsed = None
    start, end = cfg.get('started_at'), cfg.get('accepted_at')
    if start is not None:
        start = iso(start)
    if end is not None:
        end = iso(end)
    if start is not None and end is not None:
        elapsed = (end - start).total_seconds()
        if elapsed < 0:
            raise ValueError('accepted_at precedes started_at')
    result = {
        'schema': 'agent-usage-report.v1', 'task_id': state['task_id'],
        'scope': cfg['scope'], 'root_turn_ids': roots,
        'coverage': 'declared_sources', 'complete': True,
        'coverage_limits': ['Only declared source snapshots and selected root turns are covered.',
                            'Unlisted descendants and omitted coordinator/setup work cannot be detected.',
                            'Completeness describes evidence, not operator-reported outcome quality.'],
        'outcome': {key: outcome.get(key) for key in ('status', 'quality', 'rework')},
        'acceptance_refs': refs, 'acceptance_refs_verified': False,
        'outcome_basis': 'operator_reported', 'cost_usd': None,
        'task_elapsed_seconds': elapsed, 'observed_span_seconds': None,
        'totals': totals(), 'by_model_effort': [], 'sources': [], 'warnings': [],
    }
    seen, models, times, observed_roots = {}, {}, [], set()

    def warn(message):
        result['complete'] = False
        result['warnings'].append(message)

    for index, spec in enumerate(specs):
        if not isinstance(spec, dict) or not nonempty(spec.get('label')):
            raise ValueError('each source requires a path and nonempty label')
        path = resolve_path(base, spec.get('path'))
        source = {'path': str(path.absolute()), 'label': spec['label'],
                  'snapshot_bytes': None, 'sha256': None, 'read_at': None,
                  'complete': True, 'pending_final_line': False, 'totals': totals(),
                  'by_model_effort': [], 'warnings': [], 'ordinal_continuity': 'unavailable'}
        result['sources'].append(source)
        source_models = {}

        def problem(message):
            source['complete'] = False
            source['warnings'].append(message)
            warn(f'source {index}: {message}')

        try:
            with path.open('rb') as stream:
                size = stream.seek(0, 2)
                stream.seek(0)
                data = stream.read(size)
            source.update(snapshot_bytes=size, sha256=hashlib.sha256(data).hexdigest(),
                          read_at=datetime.now(timezone.utc).isoformat())
            if len(data) != size:
                problem('source shrank during snapshot')
        except OSError as exc:
            problem(f'cannot read source ({type(exc).__name__})')
            continue
        lines = data.splitlines(keepends=True)
        if lines and not lines[-1].endswith(b'\n'):
            source['pending_final_line'] = True
            problem('unterminated final line excluded as pending/truncated')
            lines.pop()
        meta, contexts, selected, completed, started, used = None, {}, set(), set(), set(), set()
        source_matches = 0
        last_ordinal = -1
        ordinal_records = {}
        missing_ordinal = False
        for lineno, raw in enumerate(lines, 1):
            try:
                item = json.loads(raw, object_pairs_hook=unique_object,
                                  parse_constant=invalid_constant)
                if not isinstance(item, dict) or not isinstance(item.get('payload'), dict):
                    raise ValueError('record/payload must be objects')
                if 'ordinal' in item:
                    ordinal = item['ordinal']
                    if type(ordinal) is not int or ordinal < 0:
                        raise ValueError('invalid source ordinal')
                    if ordinal in ordinal_records and ordinal_records[ordinal] == item:
                        continue  # Exact replay of a source record is harmless.
                    if ordinal <= last_ordinal:
                        raise ValueError('conflicting or decreasing source ordinal')
                    source['ordinal_continuity'] = 'checked'
                    if missing_ordinal:
                        problem(f'line {lineno}: mixed provided and missing source ordinals')
                    if ordinal != last_ordinal + 1:
                        problem(f'line {lineno}: source ordinal gap (expected {last_ordinal + 1})')
                    ordinal_records[ordinal] = item
                    last_ordinal = ordinal
                else:
                    missing_ordinal = True
                    if ordinal_records:
                        problem(f'line {lineno}: missing source ordinal')
                payload, kind = item['payload'], item.get('type')
                if kind == 'session_meta':
                    if not nonempty(payload.get('id')):
                        raise ValueError('session metadata missing thread id')
                    identity = (payload['id'], payload.get('session_id'))
                    if meta is not None and identity != meta:
                        raise ValueError('conflicting session metadata')
                    meta = identity
                elif kind == 'turn_context':
                    turn = payload.get('turn_id')
                    root = payload.get('root_turn_id')
                    if not nonempty(root):
                        raise ValueError('turn context missing root_turn_id; selection unknown')
                    if root in roots:
                        if not nonempty(turn):
                            raise ValueError('selected turn context missing turn id')
                        selected.add(turn)
                        if not nonempty(payload.get('model')) or not nonempty(payload.get('effort')):
                            problem(f'line {lineno}: selected context missing model/effort')
                    if nonempty(turn):
                        contexts[turn] = (payload.get('root_turn_id'), payload.get('model'), payload.get('effort'))
                elif kind == 'event_msg' and payload.get('type') in ('task_started', 'task_complete'):
                    attribution = payload.get('turn_attribution') or {}
                    if not isinstance(attribution, dict):
                        raise ValueError('invalid turn_attribution')
                    root = payload.get('root_turn_id', attribution.get('root_turn_id'))
                    turn = payload.get('turn_id', attribution.get('turn_id'))
                    if root in roots:
                        if not nonempty(turn):
                            raise ValueError('selected event missing turn id')
                        selected.add(turn)
                        if payload['type'] == 'task_started':
                            if turn in started or turn in completed:
                                problem(f'line {lineno}: repeated start or start after completion')
                            started.add(turn)
                        else:
                            if turn not in started or turn in completed:
                                problem(f'line {lineno}: completion without active start')
                            completed.add(turn)
                elif kind == 'token_usage_record':
                    root = payload.get('root_turn_id')
                    if not nonempty(root):
                        raise ValueError('usage missing root_turn_id; selection unknown')
                    if root not in roots:
                        continue
                    source_matches += 1
                    observed_roots.add(root)
                    for key in ('thread_id', 'turn_id', 'session_id', 'response_id'):
                        if not nonempty(payload.get(key)):
                            raise ValueError(f'selected usage missing {key}')
                    turn = payload['turn_id']
                    selected.add(turn)
                    used.add(turn)
                    if meta is None or payload['thread_id'] != meta[0]:
                        raise ValueError('usage thread does not match preceding session metadata')
                    if meta[1] is not None and payload['session_id'] != meta[1]:
                        raise ValueError('usage session does not match session metadata')
                    context = contexts.get(turn)
                    model = effort = None
                    if context is None or context[0] != root:
                        problem(f'line {lineno}: missing matching preceding turn context')
                    else:
                        _, model, effort = context
                        if not nonempty(model) or not nonempty(effort):
                            model = model if nonempty(model) else None
                            effort = effort if nonempty(effort) else None
                            problem(f'line {lineno}: unknown observed model/effort')
                    usage = counters(payload.get('usage'))
                    if usage['input_tokens'] + usage['output_tokens'] == 0:
                        problem(f'line {lineno}: zero per-response usage')
                    stamp = iso(item.get('timestamp'))
                    identity = (payload['thread_id'], turn, payload['session_id'], root, usage, model, effort, stamp)
                    response = payload['response_id']
                    if response in seen:
                        if seen[response] != identity:
                            raise ValueError('conflicting duplicate response_id')
                        continue
                    if turn not in started or turn in completed:
                        problem(f'line {lineno}: response outside active turn lifecycle')
                    seen[response] = identity
                    times.append(stamp)
                    add(result['totals'], usage)
                    add(source['totals'], usage)
                    key = (model, effort)
                    add(models.setdefault(key, totals()), usage)
                    add(source_models.setdefault(key, totals()), usage)
            except (ValueError, TypeError, KeyError, OverflowError) as exc:
                problem(f'line {lineno}: {exc}')
        if meta is None:
            problem('missing session metadata')
        if source_matches == 0:
            problem('no usage for selected root turns in source')
        if selected - completed:
            problem('selected turns missing task_complete')
        if selected - started:
            problem('selected turns missing task_started')
        if selected - used:
            problem('selected turns missing per-response usage')
        if not source['complete'] and source['ordinal_continuity'] == 'checked':
            # Other errors also prevent claiming continuity-qualified completeness.
            source['ordinal_continuity'] = 'checked_with_incomplete_evidence'
        source['by_model_effort'] = buckets(source_models)
    for root in roots:
        if root not in observed_roots:
            warn(f'root turn {root}: no selected usage observed')
    if result['totals']['responses'] == 0:
        warn('no valid selected responses')
    if times:
        result['observed_span_seconds'] = (max(times) - min(times)).total_seconds()
    result['by_model_effort'] = buckets(models)
    return result


def buckets(groups):
    return [dict(model=model, effort=effort, totals=value)
            for (model, effort), value in groups.items()]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record')
    parser.add_argument('--output')
    args = parser.parse_args(argv)
    try:
        value = report(args.record)
    except (ValueError, OSError) as exc:
        value = {'schema': 'agent-usage-report.v1', 'complete': False, 'warnings': [str(exc)]}
    rendered = json.dumps(value, indent=2, allow_nan=False) + '\n'
    if args.output:
        try:
            with Path(args.output).expanduser().open('x') as stream:
                stream.write(rendered)
        except OSError as exc:
            print(f'cannot create output: {exc}', file=sys.stderr)
            return 2
    else:
        print(rendered, end='')
    return 0 if value['complete'] else 1


if __name__ == '__main__':
    sys.exit(main())
