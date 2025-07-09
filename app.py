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