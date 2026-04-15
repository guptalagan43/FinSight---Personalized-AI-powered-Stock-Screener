"""
FinSight Service – Builds and executes stock screening queries.
Thin wrapper around the screener model for separation of concerns.
"""
from models.screener import run_screener as _run, get_predefined, get_user_screeners, create_screener


def execute_screen(definition_json: str) -> list:
    """Run a screener and return matching instruments."""
    return _run(definition_json)
