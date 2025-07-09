import streamlit as st
import pandas as pd

from utils.calculations import calculate_umbrella_salary, calculate_ltd_salary
from utils.charts import create_pie_chart, create_bar_chart
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="IR35 Contractor Salary Calculator", layout="centered")

st.title("💼 IR35 Contractor Salary Calculator")

tabs = st.tabs(["Inside IR35 (Umbrella)", "Outside IR35 (Ltd Co)", "Comparison"])

# --- Common Input ---
with st.sidebar:
    st.header("🔧 Contract Details")
    rate_type = st.radio("Rate Type", ["Daily", "Hourly"])
    rate = st.number_input(f"{rate_type} Rate (£)", min_value=0.0, value=500.0)
    days_per_week = st.slider("Days/Week", 1, 7, 5)
    weeks_per_year = st.slider("Weeks/Year", 30, 52, 46)
    additional_deductions = st.number_input("Other Annual Deductions (£)", 0.0, value=0.0)

# --- Inside IR35 Tab ---
with tabs[0]:
    st.subheader("Inside IR35 via Umbrella")

    emp_pension = st.slider("Employee Pension (%)", 0.0, 10.0, 0.0, step=0.5)
    er_pension = st.slider("Employer Pension (%)", 0.0, 5.0, 0.0, step=0.5)

    if st.button("Calculate Umbrella Salary"):
        umbrella = calculate_umbrella_salary(
            rate, rate_type.lower(), days_per_week, weeks_per_year,
            emp_pension_pct=emp_pension, er_pension_pct=er_pension,
            additional_deductions=additional_deductions
        )

        df = pd.DataFrame(umbrella.items(), columns=["Item", "Amount (£)"])
        st.dataframe(df, use_container_width=True)

        pie_labels = ["Income Tax", "Employee NI", "Employee Pension", "Other Deductions", "Net Annual Pay"]
        fig1 = create_pie_chart(umbrella, pie_labels)
        st.pyplot(fig1)

        bar_labels = ["Adjusted Gross", "Net Annual Pay"]
        fig2 = create_bar_chart(bar_labels, [umbrella["Adjusted Gross"], umbrella["Net Annual Pay"]], title="Umbrella Overview")
        st.pyplot(fig2)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="umbrella_breakdown.csv", mime="text/csv")

        pdf_buffer = generate_pdf("Umbrella Salary Report", umbrella, model="Umbrella")
        st.download_button("📄 Download PDF", data=pdf_buffer, file_name="umbrella_salary.pdf", mime="application/pdf")

# --- Outside IR35 Tab ---
with tabs[1]:
    st.subheader("Outside IR35 via Ltd Company")

    ltd_salary = st.number_input("Director's Salary (£)", value=12000.0, step=1000.0)
    dividend_tax_rate = st.slider("Dividend Tax Rate (%)", 0.0, 50.0, 8.75, step=0.25)

    if st.button("Calculate Ltd Company Salary"):
        ltd = calculate_ltd_salary(
            rate, rate_type.lower(), days_per_week, weeks_per_year,
            salary=ltd_salary, dividend_tax_rate=dividend_tax_rate / 100.0
        )

        df2 = pd.DataFrame(ltd.items(), columns=["Item", "Amount (£)"])
        st.dataframe(df2, use_container_width=True)

        pie_labels_ltd = ["Corporation Tax", "Dividend Tax", "Salary", "Dividends (Net)"]
        fig3 = create_pie_chart(ltd, pie_labels_ltd)
        st.pyplot(fig3)

        bar_labels = ["Salary", "Total Net Income"]
        fig4 = create_bar_chart(bar_labels, [ltd["Salary"], ltd["Total Net Income"]], title="Ltd Co Overview")
        st.pyplot(fig4)

        csv2 = df2.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv2, file_name="ltd_breakdown.csv", mime="text/csv")

        pdf_buffer = generate_pdf("Ltd Company Salary Report", ltd, model="Ltd Company")
        st.download_button("📄 Download PDF", data=pdf_buffer, file_name="ltd_salary.pdf", mime="application/pdf")

# --- Comparison Tab ---
with tabs[2]:
    st.subheader("Umbrella vs Ltd Company: Net Pay Comparison")

    if st.button("Compare Both Models"):
        umbrella = calculate_umbrella_salary(
            rate, rate_type.lower(), days_per_week, weeks_per_year,
            emp_pension_pct=emp_pension, er_pension_pct=er_pension,
            additional_deductions=additional_deductions
        )
        ltd = calculate_ltd_salary(
            rate, rate_type.lower(), days_per_week, weeks_per_year,
            salary=ltd_salary, dividend_tax_rate=dividend_tax_rate / 100.0
        )

        st.markdown("### 📊 Summary Table")
        comp_data = {
            "Model": ["Umbrella", "Ltd Company"],
            "Net Annual (£)": [umbrella["Net Annual Pay"], ltd["Total Net Income"]],
            "Monthly Take-Home (£)": [umbrella["Monthly Take-Home"], ltd["Monthly Take-Home"]],
        }
        df_comp = pd.DataFrame(comp_data)
        st.dataframe(df_comp, use_container_width=True)

        fig_comp = create_bar_chart(
            ["Umbrella", "Ltd Company"],
            [umbrella["Net Annual Pay"], ltd["Total Net Income"]],
            title="Net Annual Income Comparison"
        )
        st.pyplot(fig_comp)

        csv_comp = df_comp.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Comparison CSV", data=csv_comp, file_name="comparison.csv", mime="text/csv")

        # Merge umbrella and ltd into one dict for PDF export
        pdf_data = {
            "Umbrella Net Pay": umbrella["Net Annual Pay"],
            "Ltd Co Net Pay": ltd["Total Net Income"],
            "Umbrella Monthly": umbrella["Monthly Take-Home"],
            "Ltd Monthly": ltd["Monthly Take-Home"],
        }
        pdf_buffer = generate_pdf("Umbrella vs Ltd Summary", pdf_data, model="Comparison")
        st.download_button("📄 Download Comparison PDF", data=pdf_buffer, file_name="comparison.pdf", mime="application/pdf")

# --- Footer ---
st.markdown("""<hr style='margin-top:2em;margin-bottom:1em'>
<div style='text-align:center;color:gray;'>
Built with ❤️ using Streamlit | © 2025 scoutch007
</div>
""", unsafe_allow_html=True)