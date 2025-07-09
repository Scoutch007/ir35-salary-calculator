def calculate_umbrella_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                              employee_pension_percent=0.0, employer_pension_percent=0.0,
                              additional_deductions=0.0):
    # Convert rate to annual income
    if rate_type == 'daily':
        annual_contract_income = rate * days_per_week * weeks_per_year
    elif rate_type == 'hourly':
        annual_contract_income = rate * 8 * days_per_week * weeks_per_year
    else:  # weekly
        annual_contract_income = rate * weeks_per_year

    # Employer costs
    employer_ni_threshold = 9670
    employer_ni_rate = 0.138
    employer_ni = max((annual_contract_income - employer_ni_threshold) * employer_ni_rate, 0)
    employer_pension = annual_contract_income * (employer_pension_percent / 100)
    total_employer_costs = employer_ni + employer_pension

    gross_pay = annual_contract_income - total_employer_costs

    # Employee deductions
    employee_pension = gross_pay * (employee_pension_percent / 100)

    # Income tax (2025/26 UK thresholds)
    tax_free_allowance = 12570
    basic_rate = 0.20
    higher_rate = 0.40
    additional_rate = 0.45
    basic_threshold = 50270
    higher_threshold = 125140

    taxable_income = max(gross_pay - tax_free_allowance - employee_pension, 0)

    if gross_pay > 100000:
        # Reduce personal allowance £1 for every £2 over £100k
        reduction = (gross_pay - 100000) / 2
        tax_free_allowance = max(0, tax_free_allowance - reduction)
        taxable_income = max(gross_pay - tax_free_allowance - employee_pension, 0)

    tax = 0
    if taxable_income <= (basic_threshold - tax_free_allowance):
        tax = taxable_income * basic_rate
    elif taxable_income <= (higher_threshold - tax_free_allowance):
        tax = ((basic_threshold - tax_free_allowance) * basic_rate) + ((taxable_income - (basic_threshold - tax_free_allowance)) * higher_rate)
    else:
        tax = ((basic_threshold - tax_free_allowance) * basic_rate) + \
              ((higher_threshold - basic_threshold) * higher_rate) + \
              ((taxable_income - (higher_threshold - tax_free_allowance)) * additional_rate)

    # National Insurance (2025/26 employee NI)
    ni_threshold = 12570
    ni_rate = 0.08  # Class 1 employee NIC
    employee_ni = max((gross_pay - ni_threshold) * ni_rate, 0)

    net_income = gross_pay - tax - employee_ni - employee_pension - additional_deductions
    monthly_take_home = net_income / 12
    weekly_take_home = net_income / weeks_per_year

    return {
        "Annual Contract Income": round(annual_contract_income, 2),
        "Gross Pay": round(gross_pay, 2),
        "Employer NI": round(employer_ni, 2),
        "Employer Pension": round(employer_pension, 2),
        "Employee Pension": round(employee_pension, 2),
        "Tax": round(tax, 2),
        "Employee NI": round(employee_ni, 2),
        "Additional Deductions": round(additional_deductions, 2),
        "Net Income": round(net_income, 2),
        "Monthly Take-Home": round(monthly_take_home, 2),
        "Weekly Take-Home": round(weekly_take_home, 2)
    }


def calculate_ltd_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                         salary=12000.0, dividend_tax_rate=0.0875):
    # Gross contract income
    if rate_type == 'daily':
        gross_income = rate * days_per_week * weeks_per_year
    elif rate_type == 'hourly':
        gross_income = rate * 8 * days_per_week * weeks_per_year
    else:  # weekly
        gross_income = rate * weeks_per_year

    # Business expenses estimate
    expenses = 1000.0

    # Profit before tax
    profit_before_tax = gross_income - salary - expenses

    # Corporation Tax (2025/26 marginal relief)
    lower_limit = 50000
    upper_limit = 250000
    small_rate = 0.19
    main_rate = 0.25
    marginal_relief_fraction = 0.015  # 3/200

    if profit_before_tax <= lower_limit:
        corp_tax = profit_before_tax * small_rate
    elif profit_before_tax >= upper_limit:
        corp_tax = profit_before_tax * main_rate
    else:
        relief = (upper_limit - profit_before_tax) * marginal_relief_fraction
        effective_rate = main_rate - (relief / profit_before_tax)
        corp_tax = profit_before_tax * effective_rate

    post_tax_profit = profit_before_tax - corp_tax

    # Dividend tax
    dividend_tax = post_tax_profit * dividend_tax_rate
    net_dividends = post_tax_profit - dividend_tax

    total_net_income = net_dividends + salary
    monthly_take_home = total_net_income / 12
    weekly_take_home = total_net_income / weeks_per_year

    return {
        "Gross Contract Income": round(gross_income, 2),
        "Salary": round(salary, 2),
        "Expenses": round(expenses, 2),
        "Profit Before Tax": round(profit_before_tax, 2),
        "Corporation Tax": round(corp_tax, 2),
        "Post-Tax Profit": round(post_tax_profit, 2),
        "Dividend Tax": round(dividend_tax, 2),
        "Dividends (Net)": round(net_dividends, 2),
        "Total Net Income": round(total_net_income, 2),
        "Monthly Take-Home": round(monthly_take_home, 2),
        "Weekly Take-Home": round(weekly_take_home, 2)
    }