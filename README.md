# 💼 IR35 Umbrella Salary Calculator (2025/26)

A web-based salary calculator for UK contractors working inside or outside IR35 — built using **Streamlit**. Compare take-home pay via **Umbrella** vs **Ltd Company**, factoring in tax, pension contributions, and national insurance (NI) for the 2025/26 tax year.

---

## 🚀 Live App

👉 [Launch the calculator](https://YOUR-STREAMLIT-APP-URL)

---

## ✨ Features

- 📅 Supports **hourly** or **daily** rates
- 🔍 Models both **inside IR35 (Umbrella)** and **outside IR35 (Ltd Company)**
- 📈 Visual breakdown via pie and bar charts
- 📄 Export results as **PDF** or **CSV**
- 💰 Customise:
  - Employee/employer pension %
  - Additional deductions
  - Dividend tax rate (Ltd)
- 📊 Compare **net annual** and **monthly take-home** between models

---

## 📷 Screenshots

> _Optional: Add screenshots of the app UI_

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) – Python web app framework
- `pandas`, `matplotlib` – Data and charts
- `reportlab` – PDF generation

---

## 📦 Installation (for developers)

```bash
# Clone the repo
git clone https://github.com/scoutch007/ir35-salary-calculator.git
cd ir35-salary-calculator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
