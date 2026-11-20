
import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEARCH_FILE = PROJECT_ROOT / "Day-04" / "app" / "smart_search.py"

spec = importlib.util.spec_from_file_location(
    "smart_search_module", SEARCH_FILE
)
search_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_module)

smart_search = search_module.smart_search


def test_search_returns_results():
    results = smart_search("gratuity calculation")
    assert len(results) > 0


def test_search_respects_limit():
    results = smart_search("gratuity", limit=2)
    assert len(results) <= 2


def test_search_returns_empty_for_unknown_query():
    results = smart_search("xyzqwerty123456")
    assert results == []
