
import importlib.util
from pathlib import Path

import pytest

# Locate Day-09 tools.py directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_FILE = PROJECT_ROOT / "Day-09" / "app" / "tools.py"

spec = importlib.util.spec_from_file_location(
    "day09_tools",
    TOOLS_FILE
)

tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)

gratuity_and_wage_calculator = tools.gratuity_and_wage_calculator


# Test 1: Normal gratuity calculation
def test_gratuity_calculation():
    result = gratuity_and_wage_calculator(
        total_monthly_pay=50000,
        excluded_allowances=30000,
        completed_years=10
    )

    assert result["adjusted_monthly_wages"] == 25000
    assert result["gratuity_payable"] == 144230.77


# Test 2: Allowances within 50% threshold
def test_allowances_within_threshold():
    result = gratuity_and_wage_calculator(
        total_monthly_pay=50000,
        excluded_allowances=20000,
        completed_years=10
    )

    assert result["excess_allowances_added_back"] == 0
    assert result["adjusted_monthly_wages"] == 30000


# Test 3: Maximum gratuity cap
def test_maximum_gratuity_limit():
    result = gratuity_and_wage_calculator(
        total_monthly_pay=100000,
        excluded_allowances=0,
        completed_years=40
    )

    assert result["gratuity_payable"] == 2000000
    assert result["maximum_limit"] == 2000000


# Test 4: Negative monthly pay
def test_negative_monthly_pay():
    with pytest.raises(ValueError):
        gratuity_and_wage_calculator(
            total_monthly_pay=-50000,
            excluded_allowances=0,
            completed_years=10
        )


# Test 5: Excluded allowances cannot exceed total pay
def test_excluded_allowances_exceed_total_pay():
    with pytest.raises(ValueError):
        gratuity_and_wage_calculator(
            total_monthly_pay=50000,
            excluded_allowances=60000,
            completed_years=10
        )


# Test 6: Negative completed years
def test_negative_completed_years():
    with pytest.raises(ValueError):
        gratuity_and_wage_calculator(
            total_monthly_pay=50000,
            excluded_allowances=20000,
            completed_years=-5
        )
