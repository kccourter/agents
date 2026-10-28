"""Read the single canonical agent-task block; no state mutation or dispatch."""
from __future__ import annotations

import json
from pathlib import Path
import re


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"non-finite JSON number: {value}")


def load_record(path):
    """Return (state, record directory); reject ambiguous or malformed state."""
    record = Path(path).expanduser().resolve(strict=True)
    text = record.read_text()
    blocks = re.findall(r"^```agent-task[ \t]*\r?\n(.*?)^```[ \t]*$",
                        text, re.MULTILINE | re.DOTALL)
    if len(blocks) != 1 or len(re.findall(r"^```agent-task[ \t]*$", text, re.MULTILINE)) != 1:
        raise ValueError("record must contain exactly one agent-task JSON fence")
    state = json.loads(blocks[0], object_pairs_hook=unique_object,
                       parse_constant=invalid_constant)
    if not isinstance(state, dict) or state.get("schema") != "agent-task.v1":
        raise ValueError("expected schema agent-task.v1")
    for key in ("task_id", "outcome", "next_action"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    if state.get("status") not in {"planned", "active", "blocked", "accepted"}:
        raise ValueError("status must be planned, active, blocked, or accepted")
    for key in ("constraints", "decisions", "repositories", "assignments",
                "processes", "findings", "checks"):
        if not isinstance(state.get(key, []), list):
            raise ValueError(f"{key} must be a list")
    for key in ("resources", "usage"):
        if key in state and not isinstance(state[key], dict):
            raise ValueError(f"{key} must be an object")
    return state, record.parent


def resolve_path(base, value):
    if not isinstance(value, str) or not value:
        raise ValueError("path must be a nonempty string")
    path = Path(value).expanduser()
    # Do not resolve symlinks here: callers must inspect watched path types.
    return path if path.is_absolute() else Path(base) / path
