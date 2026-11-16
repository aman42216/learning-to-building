
MAX_GRATUITY = 2000000


def gratuity_and_wage_calculator(
    total_monthly_pay,
    excluded_allowances,
    completed_years
):
    """
    Calculate adjusted wages and gratuity.

    Wages = (Total Pay - Excluded Allowances)
            + excess excluded allowances above 50% of total pay

    Gratuity = 15/26 x Monthly Wages x Completed Years
    Maximum gratuity = Rs. 20 lakh
    """

    if total_monthly_pay < 0:
        raise ValueError("Total monthly pay cannot be negative")

    if excluded_allowances < 0:
        raise ValueError("Excluded allowances cannot be negative")

    if excluded_allowances > total_monthly_pay:
        raise ValueError(
            "Excluded allowances cannot exceed total monthly pay"
        )

    if completed_years < 0:
        raise ValueError("Completed years cannot be negative")

    # Calculate 50% wage threshold
    allowance_limit = total_monthly_pay * 0.50

    # Calculate excess allowances
    excess_allowances = max(
        0,
        excluded_allowances - allowance_limit
    )

    # Adjust monthly wages
    adjusted_monthly_wages = (
        total_monthly_pay
        - excluded_allowances
        + excess_allowances
    )

    # Calculate gratuity
    gratuity_before_cap = (
        (15 / 26)
        * adjusted_monthly_wages
        * completed_years
    )

    # Apply Rs. 20 lakh maximum limit
    final_gratuity = min(
        gratuity_before_cap,
        MAX_GRATUITY
    )

    return {
        "total_monthly_pay": round(total_monthly_pay, 2),
        "excluded_allowances": round(excluded_allowances, 2),
        "excess_allowances_added_back": round(excess_allowances, 2),
        "adjusted_monthly_wages": round(
            adjusted_monthly_wages, 2
        ),
        "completed_years": completed_years,
        "gratuity_before_cap": round(gratuity_before_cap, 2),
        "gratuity_payable": round(final_gratuity, 2),
        "maximum_limit": MAX_GRATUITY
    }


if __name__ == "__main__":

    result = gratuity_and_wage_calculator(
        total_monthly_pay=50000,
        excluded_allowances=30000,
        completed_years=10
    )

    print("Gratuity Calculation Result")
    print("---------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
