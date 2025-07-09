import streamlit as st

def calculate_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                     emp_pension_pct=0.0, er_pension_pct=0.0, additional_deductions=0.0):
    # Constants
    umbrella_margin = 25 * weeks_per_year
    employer_ni_rate = 0.138
    employee_ni_threshold = 12570
    employee_ni_rate = 0.12
    employee_ni_upper_rate = 0.02
    income_tax_bands = [(12570, 0.0), (50270, 0.20), (125140, 0.40)]
    personal_allowance = 12570

    # Gross income from rate
    if rate_type == 'daily':
        annual_contract_income = rate * days_per_week * weeks_per_year
    else:
        annual_contract_income = rate * 8 * days_per_week * weeks_per_year

    # Employer NI and pension contributions
    employer_ni = annual_contract_income * employer_ni_rate
    employer_pension = annual_contract_income * (er_pension_pct / 100.0)

    adjusted_gross = annual_contract_income - employer_ni - umbrella_margin + employer_pension

    # Employee pension deduction
    employee_pension = adjusted_gross * (emp_pension_pct / 100.0)

    # Taxable income
    taxable_income = max(0, adjusted_gross - personal_allowance - employee_pension)
    tax_due = 0
    prev_band_limit = 12570

    for band_limit, rate_val in income_tax_bands[1:]:
        if taxable_income > band_limit:
            tax_due += (band_limit - prev_band_limit) * rate_val
            prev_band_limit = band_limit
        else:
            tax_due += (taxable_income - prev_band_limit) * rate_val
            break

    # National Insurance
    ni_due = 0
    if adjusted_gross > employee_ni_threshold:
        ni_taxable = adjusted_gross - employee_ni_threshold
        ni_due = (
            min(ni_taxable, 37700) * employee_ni_rate +
            max(0, ni_taxable - 37700) * employee_ni_upper_rate
        )

    # Net pay
    net_pay = adjusted_gross - tax_due - ni_due - employee_pension - additional_deductions

    return {
        "Annual Contract Income": round(annual_contract_income, 2),
        "Umbrella Margin (Annual)": round(umbrella_margin, 2),
        "Employer NI": round(employer_ni, 2),
        "Employer Pension Contribution": round(employer_pension, 2),
        "Gross After Employer Deductions": round(adjusted_gross, 2),
        "Employee Pension Deduction": round(employee_pension, 2),
        "Income Tax Due": round(tax_due, 2),
        "Employee NI": round(ni_due, 2),
        "Other Deductions": round(additional_deductions, 2),
        "Net Annual Pay": round(net_pay, 2),
        "Monthly Take-Home": round(net_pay / 12, 2)
    }

# ---- Streamlit Interface ----

st.set_page_config(page_title="IR35 Umbrella Salary Calculator", layout="centered")

st.title("💼 Contractor Salary Calculator (Inside IR35 via Umbrella)")
st.markdown("""
This calculator estimates your **net pay** when working **inside IR35** via an **umbrella company**, with options for:
- Hourly or daily rate
- Pension contributions (employee and employer)
- Additional deductions (e.g. student loan, insurance)
""")

# User inputs
rate_type = st.radio("Rate Type", ['Daily', 'Hourly'])
rate = st.number_input(f"Enter your {rate_type.lower()} rate (£)", min_value=0.0, value=500.0, step=10.0)
days_per_week = st.slider("Working Days per Week", 1, 7, 5)
weeks_per_year = st.slider("Working Weeks per Year", 30, 52, 46)

st.markdown("### 🏦 Pension Contributions")
emp_pension_pct = st.slider("Employee Pension (%)", 0.0, 10.0, 0.0, step=0.5)
er_pension_pct = st.slider("Employer Pension (%)", 0.0, 5.0, 0.0, step=0.5)

st.markdown("### 🧾 Other Deductions")
additional_deductions = st.number_input("Other Annual Deductions (£)", min_value=0.0, value=0.0, step=100.0)

# Calculate button
if st.button("Calculate"):
    result = calculate_salary(
        rate=rate,
        rate_type=rate_type.lower(),
        days_per_week=days_per_week,
        weeks_per_year=weeks_per_year,
        emp_pension_pct=emp_pension_pct,
        er_pension_pct=er_pension_pct,
        additional_deductions=additional_deductions
    )

    st.subheader("📊 Results")
    for key, value in result.items():
        st.write(f"**{key}:** £{value:,.2f}")
