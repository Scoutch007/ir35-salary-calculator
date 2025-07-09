def calculate_umbrella_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                              emp_pension_pct=0.0, er_pension_pct=0.0, additional_deductions=0.0):
    umbrella_margin = 25 * weeks_per_year
    employer_ni_rate = 0.138
    employee_ni_threshold = 12570
    employee_ni_rate = 0.12
    employee_ni_upper_rate = 0.02
    personal_allowance = 12570
    income_tax_bands = [(12570, 0.0), (50270, 0.20), (125140, 0.40)]

    if rate_type == 'daily':
        annual_contract_income = rate * days_per_week * weeks_per_year
    else:
        annual_contract_income = rate * 8 * days_per_week * weeks_per_year

    employer_ni = annual_contract_income * employer_ni_rate
    employer_pension = annual_contract_income * (er_pension_pct / 100.0)
    adjusted_gross = annual_contract_income - employer_ni - umbrella_margin + employer_pension
    employee_pension = adjusted_gross * (emp_pension_pct / 100.0)
    taxable_income = max(0, adjusted_gross - personal_allowance - employee_pension)

    tax_due = 0
    prev_limit = 12570
    for limit, rate_val in income_tax_bands[1:]:
        if taxable_income > limit:
            tax_due += (limit - prev_limit) * rate_val
            prev_limit = limit
        else:
            tax_due += (taxable_income - prev_limit) * rate_val
            break

    ni_due = 0
    if adjusted_gross > employee_ni_threshold:
        ni_taxable = adjusted_gross - employee_ni_threshold
        ni_due = (
            min(ni_taxable, 37700) * employee_ni_rate +
            max(0, ni_taxable - 37700) * employee_ni_upper_rate
        )

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


def calculate_ltd_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                         salary=12000, dividend_tax_rate=0.0875):
    corp_tax_rate = 0.19
    if rate_type == 'daily':
        annual_income = rate * days_per_week * weeks_per_year
    else:
        annual_income = rate * 8 * days_per_week * weeks_per_year

    corp_expenses = salary
    profit_before_tax = annual_income - corp_expenses
    corporation_tax = profit_before_tax * corp_tax_rate
    post_tax_profit = profit_before_tax - corporation_tax

    dividends = post_tax_profit
    dividend_tax = dividends * dividend_tax_rate
    net_dividends = dividends - dividend_tax

    total_net = salary + net_dividends

    return {
        "Annual Contract Income": round(annual_income, 2),
        "Salary": round(salary, 2),
        "Corporation Tax": round(corporation_tax, 2),
        "Dividends (Net)": round(net_dividends, 2),
        "Dividend Tax": round(dividend_tax, 2),
        "Total Net Income": round(total_net, 2),
        "Monthly Take-Home": round(total_net / 12, 2)
    }
