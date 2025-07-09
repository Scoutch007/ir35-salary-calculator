import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="IR35 Umbrella Salary Calculator", layout="centered")

def calculate_salary(rate, rate_type='daily', days_per_week=5, weeks_per_year=46,
                     emp_pension_pct=0.0, er_pension_pct=0.0, additional_deductions=0.0):
    umbrella_margin = 25 * weeks_per_year
    employer_ni_rate = 0.138
    employee_ni_threshold = 12570
    employee_ni_rate = 0.12
    employee_ni_upper_rate = 0.02
    income_tax_bands = [(12570, 0.0), (50270, 0.20), (125140, 0.40)]
    personal_allowance = 12570

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
    prev_band_limit = 12570

    for band_limit, rate_val in income_tax_bands[1:]:
        if taxable_income > band_limit:
            tax_due += (band_limit - prev_band_limit) * rate_val
            prev_band_limit = band_limit
        else:
            tax_due += (taxable_income - prev_band_limit) * rate_val
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

# --- Streamlit Interface ---
st.title("💼 Contractor Salary Calculator (Inside IR35 via Umbrella)")

st.markdown("""
This calculator estimates your **net take-home pay** based on your contract rate, pension contributions, and common deductions when working **inside IR35** via an umbrella company.
""")

# --- Session state defaults ---
if 'rate_type' not in st.session_state:
    st.session_state.rate_type = 'Daily'

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    rate_type = st.radio("Rate Type", ['Daily', 'Hourly'], key='rate_type')
    rate = st.number_input(f"{rate_type} Rate (£)", min_value=0.0, value=500.0)
    emp_pension_pct = st.slider("Employee Pension (%)", 0.0, 10.0, 0.0, step=0.5)
    er_pension_pct = st.slider("Employer Pension (%)", 0.0, 5.0, 0.0, step=0.5)

with col2:
    days_per_week = st.slider("Working Days/Week", 1, 7, 5)
    weeks_per_year = st.slider("Working Weeks/Year", 30, 52, 46)
    additional_deductions = st.number_input("Other Annual Deductions (£)", min_value=0.0, value=0.0, step=100.0)

# --- Calculate ---
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

    st.subheader("📊 Salary Breakdown")
    df_result = pd.DataFrame(result.items(), columns=["Item", "Amount (£)"])
    st.dataframe(df_result, use_container_width=True)

    # --- Pie Chart ---
    st.markdown("### 📌 Where Your Money Goes")
    pie_labels = [
        "Income Tax", "Employee NI", "Employee Pension", "Other Deductions", "Net Pay"
    ]
    pie_values = [
        result["Income Tax Due"],
        result["Employee NI"],
        result["Employee Pension Deduction"],
        result["Other Deductions"],
        result["Net Annual Pay"]
    ]

    fig1, ax1 = plt.subplots()
    ax1.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # --- Bar Chart: Gross vs Net ---
    st.markdown("### 💰 Gross vs Net Comparison")
    bar_labels = ["Gross After Deductions", "Net Pay"]
    bar_values = [
        result["Gross After Employer Deductions"],
        result["Net Annual Pay"]
    ]
    fig2, ax2 = plt.subplots()
    ax2.bar(bar_labels, bar_values, color=["#8888ff", "#44cc44"])
    ax2.set_ylabel("£ per Year")
    st.pyplot(fig2)

    # --- CSV Export ---
    st.markdown("### 📤 Export Results")
    csv = df_result.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='ir35_salary_breakdown.csv',
        mime='text/csv'
    )
    
# --- Footer ---
st.markdown("""<hr style='margin-top:2em;margin-bottom:1em'>
<div style='text-align:center;color:gray;'>
Built with ❤️ using Streamlit | © 2025 scoutch007
</div>
""", unsafe_allow_html=True)