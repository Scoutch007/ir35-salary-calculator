import streamlit as st
from utils.calculations import calculate_umbrella_salary, calculate_ltd_salary
from utils.charts import plot_income_pie, plot_net_income_bar
from utils.export import export_to_pdf, export_to_csv

st.set_page_config(page_title="IR35 Salary Calculator", layout="centered")

st.title("💼 IR35 Umbrella & Ltd Company Salary Calculator")
st.markdown(
    "This calculator estimates your take-home pay based on your contract rate and IR35 status. "
    "Supports **daily**, **hourly**, or **weekly** rates."
)

# Sidebar Inputs
st.sidebar.header("Contract Details")
rate = st.sidebar.number_input("Contract Rate (£)", min_value=0.0, step=10.0, value=500.0)
rate_type = st.sidebar.radio("Rate Type", ["Daily", "Hourly", "Weekly"])
days_per_week = st.sidebar.slider("Days per Week", 1, 7, 5)
weeks_per_year = st.sidebar.slider("Working Weeks per Year", 1, 52, 46)

st.sidebar.header("Pension & Deductions")
employee_pension_percent = st.sidebar.slider("Employee Pension (%)", 0.0, 10.0, 0.0)
employer_pension_percent = st.sidebar.slider("Employer Pension (%)", 0.0, 10.0, 0.0)
additional_deductions = st.sidebar.number_input("Other Deductions (£/year)", 0.0, 10000.0, 0.0)

st.sidebar.header("Ltd Company Settings")
director_salary = st.sidebar.number_input("Director Salary (£/year)", 0.0, 50000.0, 12000.0)
dividend_tax_rate = st.sidebar.selectbox("Dividend Tax Rate", [0.0875, 0.3375, 0.3935], index=0,
    format_func=lambda x: f"{x*100:.2f}%")

# Tabs for comparison
tab1, tab2 = st.tabs(["🚧 Inside IR35 (Umbrella)", "🚀 Outside IR35 (Ltd Company)"])

with tab1:
    st.subheader("Inside IR35 via Umbrella Company")
    umbrella = calculate_umbrella_salary(
        rate, rate_type, days_per_week, weeks_per_year,
        employee_pension_percent, employer_pension_percent, additional_deductions
    )

    st.metric("Net Income (Annual)", f"£{umbrella['Net Income']:,.2f}")
    st.metric("Monthly Take-Home", f"£{umbrella['Monthly Take-Home']:,.2f}")
    st.metric("Weekly Take-Home", f"£{umbrella['Weekly Take-Home']:,.2f}")

    st.markdown("### Breakdown")
    st.dataframe(umbrella, use_container_width=True)
    st.markdown("### Umbrella Income Breakdown (Pie Chart)")
    st.pyplot(plot_income_pie(umbrella, "Umbrella"))

with tab2:
    st.subheader("Outside IR35 via Ltd Company")
    ltd = calculate_ltd_salary(
        rate, rate_type, days_per_week, weeks_per_year,
        director_salary, dividend_tax_rate
    )

    st.metric("Total Net Income (Annual)", f"£{ltd['Total Net Income']:,.2f}")
    st.metric("Monthly Take-Home", f"£{ltd['Monthly Take-Home']:,.2f}")
    st.metric("Weekly Take-Home", f"£{ltd['Weekly Take-Home']:,.2f}")

    st.markdown("### Breakdown")
    st.dataframe(ltd, use_container_width=True)
    st.markdown("### Ltd Company Income Breakdown (Pie Chart)")
    st.pyplot(plot_income_pie(ltd, "Ltd"))

st.markdown("## 📊 Net Income Comparison")
st.pyplot(plot_net_income_bar(umbrella, ltd))

st.markdown("---")
st.subheader("📤 Export Your Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        label="⬇️ Umbrella CSV",
        data=export_to_csv(umbrella, "Umbrella"),
        file_name="umbrella_results.csv",
        mime="text/csv"
    )

with col2:
    st.download_button(
        label="⬇️ Ltd Company CSV",
        data=export_to_csv(ltd, "Ltd"),
        file_name="ltd_results.csv",
        mime="text/csv"
    )

with col3:
    st.download_button(
        label="⬇️ Export as PDF",
        data=export_to_pdf(umbrella, ltd),
        file_name="ir35_summary.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.caption("⚖️ For guidance only. This tool does not constitute financial or tax advice.")

# --- Footer ---
st.markdown("""<hr style='margin-top:2em;margin-bottom:1em'>
<div style='text-align:center;color:gray;'>
Built with ❤️ using Streamlit | © 2025 scoutch007
</div>
""", unsafe_allow_html=True)