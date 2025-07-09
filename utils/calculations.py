def calculate_ltd_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                         salary=12000.0, dividend_tax_rate=0.0875):
    # Gross contract income
    if rate_type == 'daily':
        gross_income = rate * days_per_week * weeks_per_year
    else:
        gross_income = rate * 8 * days_per_week * weeks_per_year

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
        "Monthly Take-Home": round(monthly_take_home, 2)
    }