def calculate_umbrella_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                              emp_pension_pct=0.0, er_pension_pct=0.0, additional_deductions=0.0):
    # 2025/26 rates
    umbrella_margin = 25 * weeks_per_year
    employer_ni_rate = 0.138
    employer_ni_threshold = 9100
    employee_ni_threshold = 12570
    ni_12_rate_limit = 50270
    employee_ni_rate = 0.12
    employee_ni_upper_rate = 0.02
    personal_allowance = 12570

    income_tax_bands = [
        (personal_allowance, 0.0),   # £0–12,570
        (50270, 0.20),               # £12,571–50,270
        (125140, 0.40),              # £50,271–125,140
        (float('inf'), 0.45)         # over £125,140
    ]

    # Calculate gross income
    if rate_type == 'daily':
        annual_contract_income = rate * days_per_week * weeks_per_year
    else:
        annual_contract_income = rate * 8 * days_per_week * weeks_per_year

    # Employer side
    employer_ni = max(0, annual_contract_income - employer_ni_threshold) * employer_ni_rate
    employer_pension = annual_contract_income * (er_pension_pct / 100.0)

    # Employee side (adjusted gross)
    adjusted_gross = annual_contract_income - employer_ni - umbrella_margin + employer_pension
    employee_pension = adjusted_gross * (emp_pension_pct / 100.0)
    taxable_income = max(0, adjusted_gross - personal_allowance - employee_pension)

    # Income Tax Calculation
    tax_due = 0
    prev_limit = 0
    for limit, rate_val in income_tax_bands:
        if taxable_income > limit:
            tax_due += (limit - prev_limit) * rate_val
            prev_limit = limit
        else:
            tax_due += (taxable_income - prev_limit) * rate_val
            break

    # National Insurance (employee)
    ni_due = 0
    if adjusted_gross > employee_ni_threshold:
        ni_band = min(ni_12_rate_limit, adjusted_gross) - employee_ni_threshold
        ni_high = max(0, adjusted_gross - ni_12_rate_limit)
        ni_due = (ni_band * employee_ni_rate) + (ni_high * employee_ni_upper_rate)

    net_pay = adjusted_gross - tax_due - ni_due - employee_pension - additional_deductions

    return {
        "Annual Contract Income": round(annual_contract_income, 2),
        "Umbrella Margin": round(umbrella_margin, 2),
        "Employer NI": round(employer_ni, 2),
        "Employer Pension": round(employer_pension, 2),
        "Adjusted Gross": round(adjusted_gross, 2),
        "Employee Pension": round(employee_pension, 2),
        "Income Tax": round(tax_due, 2),
        "Employee NI": round(ni_due, 2),
        "Other Deductions": round(additional_deductions, 2),
        "Net Annual Pay": round(net_pay, 2),
        "Monthly Take-Home": round(net_pay / 12, 2)
    }
