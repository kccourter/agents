"""Behavioral tests with the observed local rollout schema and no private content."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import usage_report as u


def line(kind, payload, seconds=0):
    return {'type': kind, 'payload': payload,
            'timestamp': f'2026-10-15T22:14:{seconds:02}.000Z'}


def fixture(thread='worker', turn='turn', response='resp', seconds=1):
    return [line('session_meta', {'id': thread, 'session_id': 'session',
                                 'parent_thread_id': 'outer',
                                 'source': {'subagent': {'thread_spawn': {'agent_path': '/root/worker'}}}}),
            line('event_msg', {'type': 'task_started', 'turn_attribution':
                              {'turn_id': turn, 'root_turn_id': 'selected'}}),
            line('turn_context', {'turn_id': turn, 'root_turn_id': 'selected',
                                  'model': 'observed-model', 'effort': 'high'}),
            line('token_usage_record', {'thread_id': thread, 'turn_id': turn,
                  'session_id': 'session', 'root_turn_id': 'selected', 'response_id': response,
                  'usage': {'input_tokens': 20, 'cached_input_tokens': 12,
                            'cache_write_input_tokens': 0, 'output_tokens': 10,
                            'reasoning_output_tokens': 3, 'total_tokens': 30},
                  'turn_token_usage': {'total_tokens': 9999},
                  'thread_token_usage': {'total_tokens': 99999}}, seconds),
            line('event_msg', {'type': 'task_complete', 'turn_id': turn,
                              'root_turn_id': 'selected', 'duration_ms': 999999}, seconds + 1)]


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.cfg = {'root_turn_ids': ['selected'], 'scope': 'bounded pilot',
                    'sources': [{'path': 'source.jsonl', 'label': 'worker'}],
                    'outcome': {'status': 'accepted', 'quality': None, 'rework': None,
                                'acceptance_refs': ['receipt.json']}}
        self.write(fixture())

    def write(self, rows, name='source.jsonl', suffix=''):
        (self.base / name).write_text(''.join(json.dumps(x) + '\n' for x in rows) + suffix)

    def record(self):
        state = {'schema': 'agent-task.v1', 'task_id': 'authoritative', 'outcome': 'test',
                 'status': 'active', 'next_action': 'test', 'usage': self.cfg}
        record = self.base / 'record.md'
        record.write_text('```agent-task\n' + json.dumps(state) + '\n```\n')
        return record

    def run_report(self):
        return u.report(self.record())

    def test_actual_schema_and_unknown_quality(self):
        value = self.run_report()
        self.assertTrue(value['complete'], value['warnings'])
        self.assertEqual(value['task_id'], 'authoritative')
        self.assertEqual(value['totals']['total_tokens'], 30)
        self.assertEqual(value['totals']['uncached_input_tokens'], 8)
        self.assertEqual(value['totals']['reasoning_output_tokens'], 3)
        self.assertIsNone(value['outcome']['quality'])
        self.assertIsNone(value['cost_usd'])
        self.assertIsNone(value['task_elapsed_seconds'])
        self.assertFalse(value['acceptance_refs_verified'])
        self.assertEqual(value['coverage'], 'declared_sources')
        self.assertEqual(value['sources'][0]['snapshot_bytes'], (self.base / 'source.jsonl').stat().st_size)
        self.assertEqual(len(value['sources'][0]['sha256']), 64)

    def test_filter_other_root_and_ignore_cumulative(self):
        rows = fixture()
        other = copy.deepcopy(rows[3])
        other['payload']['root_turn_id'] = 'other'
        other['payload']['response_id'] = 'other'
        rows.insert(4, other)
        rows.insert(4, line('event_msg', {'type': 'token_count', 'info': {'total_token_usage': {'total_tokens': 9999}}}))
        self.write(rows)
        self.assertEqual(self.run_report()['totals']['total_tokens'], 30)

    def test_context_changes_and_own_turn(self):
        rows = fixture()
        rows.insert(3, line('turn_context', {'turn_id': 'different', 'root_turn_id': 'unrelated',
                                           'model': 'wrong', 'effort': 'low'}))
        rows.insert(-1, line('turn_context', {'turn_id': 'turn', 'root_turn_id': 'selected',
                                             'model': 'changed', 'effort': 'medium'}))
        second = copy.deepcopy(rows[4])
        second['payload']['response_id'] = 'second'
        rows.insert(-1, second)
        self.write(rows)
        value = self.run_report()
        self.assertTrue(value['complete'], value['warnings'])
        self.assertEqual([b['model'] for b in value['by_model_effort']], ['observed-model', 'changed'])

    def test_missing_context_is_unknown_incomplete(self):
        rows = fixture()
        del rows[2]
        self.write(rows)
        value = self.run_report()
        self.assertFalse(value['complete'])
        self.assertIsNone(value['by_model_effort'][0]['model'])
        self.assertEqual(value['totals']['responses'], 1)

    def test_duplicate_and_conflict(self):
        rows = fixture()
        rows.insert(4, copy.deepcopy(rows[3]))
        self.write(rows)
        self.assertTrue(self.run_report()['complete'])
        self.assertEqual(self.run_report()['totals']['responses'], 1)
        rows[4]['payload']['usage']['input_tokens'] += 1
        rows[4]['payload']['usage']['total_tokens'] += 1
        self.write(rows)
        self.assertFalse(self.run_report()['complete'])

    def test_identical_ordinal_replay(self):
        rows = fixture()
        for i, row in enumerate(rows):
            row['ordinal'] = i
        rows.append(copy.deepcopy(rows[3]))
        self.write(rows)
        value = self.run_report()
        self.assertTrue(value['complete'], value['warnings'])
        self.assertEqual(value['totals']['responses'], 1)

    def test_global_duplicate_across_sources(self):
        self.write(fixture(), 'second.jsonl')
        self.cfg['sources'].append({'path': 'second.jsonl', 'label': 'mirror'})
        value = self.run_report()
        self.assertTrue(value['complete'], value['warnings'])
        self.assertEqual(value['totals']['responses'], 1)
        self.assertEqual(sum(s['totals']['responses'] for s in value['sources']), 1)

    def test_invalid_ids_and_counters(self):
        mutations = [('response_id', ''), ('thread_id', 'wrong'), ('session_id', 'wrong'),
                     ('root_turn_id', None), ('turn_id', None)]
        for key, val in mutations:
            with self.subTest(key=key):
                rows = fixture()
                rows[3]['payload'][key] = val
                self.write(rows)
                self.assertFalse(self.run_report()['complete'])
        for key, val in [('input_tokens', True), ('input_tokens', 1.1),
                         ('input_tokens', -1), ('cached_input_tokens', 21),
                         ('reasoning_output_tokens', 11), ('total_tokens', 999),
                         ('output_tokens', None)]:
            with self.subTest(key=key, val=val):
                rows = fixture()
                rows[3]['payload']['usage'][key] = val
                self.write(rows)
                self.assertFalse(self.run_report()['complete'])

    def test_zero_usage_is_incomplete(self):
        rows = fixture()
        rows[3]['payload']['usage'] = dict.fromkeys(rows[3]['payload']['usage'], 0)
        self.write(rows)
        self.assertFalse(self.run_report()['complete'])

    def test_selected_context_without_lifecycle_is_incomplete(self):
        rows = fixture()
        rows.append(line('turn_context', {'turn_id': 'new-turn', 'root_turn_id': 'selected',
                                          'model': 'observed', 'effort': 'high'}))
        self.write(rows)
        value = self.run_report()
        self.assertFalse(value['complete'])
        self.assertTrue(any('missing task_complete' in w for w in value['warnings']))
        for field in ('turn_id', 'root_turn_id', 'model', 'effort'):
            with self.subTest(field=field):
                broken = copy.deepcopy(rows)
                del broken[-1]['payload'][field]
                self.write(broken)
                self.assertFalse(self.run_report()['complete'])

    def test_lifecycle_order_is_required(self):
        variants = []
        rows = fixture()
        rows.append(copy.deepcopy(rows[1]))
        variants.append(rows)
        rows = fixture()
        rows.insert(1, rows.pop())  # completion precedes start
        variants.append(rows)
        rows = fixture()
        rows.insert(2, copy.deepcopy(rows[1]))  # repeated active start
        variants.append(rows)
        rows = fixture()
        rows.append(copy.deepcopy(rows[-1]))  # repeated completion
        variants.append(rows)
        rows = fixture()
        response = rows.pop(3)
        rows.append(response)  # response after completion
        variants.append(rows)
        for index, rows in enumerate(variants):
            with self.subTest(index=index):
                self.write(rows)
                self.assertFalse(self.run_report()['complete'])

    def test_nonfinite_ignored_record_is_incomplete(self):
        for number in ('NaN', 'Infinity', '-Infinity'):
            with self.subTest(number=number):
                self.write(fixture(), suffix='{"type":"ignored","payload":{"number":' + number + '}}\n')
                self.assertFalse(self.run_report()['complete'])

    def test_ordinal_continuity(self):
        value = self.run_report()
        self.assertTrue(value['complete'])
        self.assertEqual(value['sources'][0]['ordinal_continuity'], 'unavailable')
        rows = fixture()
        for index, row in enumerate(rows):
            row['ordinal'] = index
        self.write(rows)
        self.assertTrue(self.run_report()['complete'])
        for change in ('initial-gap', 'interior-gap', 'missing-first', 'missing-interior', 'conflict'):
            with self.subTest(change=change):
                altered = copy.deepcopy(rows)
                if change == 'initial-gap':
                    for row in altered:
                        row['ordinal'] += 1
                elif change == 'interior-gap':
                    for row in altered[2:]:
                        row['ordinal'] += 1
                elif change == 'missing-first':
                    del altered[0]['ordinal']
                elif change == 'missing-interior':
                    del altered[2]['ordinal']
                else:
                    altered[-1]['ordinal'] = altered[-2]['ordinal']
                self.write(altered)
                self.assertFalse(self.run_report()['complete'])

    def test_optional_cache_write_unknown(self):
        rows = fixture()
        del rows[3]['payload']['usage']['cache_write_input_tokens']
        self.write(rows)
        value = self.run_report()
        self.assertTrue(value['complete'])
        self.assertIsNone(value['totals']['cache_write_input_tokens'])

    def test_partial_and_malformed(self):
        self.write(fixture(), suffix='{"pending":')
        value = self.run_report()
        self.assertFalse(value['complete'])
        self.assertTrue(value['sources'][0]['pending_final_line'])
        self.write(fixture(), suffix='invalid\n')
        self.assertFalse(self.run_report()['complete'])
        self.write(fixture(), suffix='{"type":"anything","payload":{},"payload":{}}\n')
        self.assertFalse(self.run_report()['complete'])

    def test_missing_completion_start_usage_source_selection(self):
        for drop in (0, 1, 3, 4):
            with self.subTest(drop=drop):
                rows = fixture()
                del rows[drop]
                self.write(rows)
                self.assertFalse(self.run_report()['complete'])
        (self.base / 'source.jsonl').unlink()
        self.assertFalse(self.run_report()['complete'])
        self.write(fixture())
        self.cfg['root_turn_ids'].append('missing')
        self.assertFalse(self.run_report()['complete'])

    def test_parallel_span_and_task_elapsed(self):
        self.write(fixture(seconds=5))
        self.write(fixture('worker2', 'turn2', 'response2', 20), 'parallel.jsonl')
        self.cfg['sources'].append({'path': 'parallel.jsonl', 'label': 'parallel'})
        self.cfg.update(started_at='2026-10-15T22:00:00Z', accepted_at='2026-10-15T22:10:00Z')
        value = self.run_report()
        self.assertTrue(value['complete'], value['warnings'])
        self.assertEqual(value['observed_span_seconds'], 15)
        self.assertEqual(value['task_elapsed_seconds'], 600)
        self.assertEqual(value['totals']['total_tokens'], 60)

    def test_cli_exclusive_output_and_nonzero(self):
        record = str(self.record())
        output = str(self.base / 'report.json')
        self.assertEqual(u.main([record, '--output', output]), 0)
        before = Path(output).read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(u.main([record, '--output', output]), 2)
        self.assertEqual(Path(output).read_bytes(), before)
        self.write([])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(u.main([record]), 1)
        self.cfg['root_turn_ids'] = []
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(u.main([str(self.record())]), 1)


if __name__ == '__main__':
    unittest.main()
