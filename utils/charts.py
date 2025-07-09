import matplotlib.pyplot as plt
import pandas as pd


def plot_income_pie(data: dict, model: str):
    labels = []
    values = []

    if model == "Umbrella":
        labels = ["Take-Home Pay", "Income Tax", "Employee NI", "Employee Pension", "Other Deductions"]
        values = [
            data["Net Income"],
            data["Tax"],
            data["Employee NI"],
            data["Employee Pension"],
            data["Additional Deductions"]
        ]
    elif model == "Ltd":
        labels = ["Take-Home Pay", "Corporation Tax", "Dividend Tax"]
        values = [
            data["Total Net Income"],
            data["Corporation Tax"],
            data["Dividend Tax"]
        ]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    return fig


def plot_net_income_bar(umbrella_data: dict, ltd_data: dict):
    labels = ["Umbrella", "Ltd Company"]
    values = [umbrella_data["Net Income"], ltd_data["Total Net Income"]]

    df = pd.DataFrame({"Model": labels, "Net Income": values})

    fig, ax = plt.subplots()
    ax.bar(df["Model"], df["Net Income"], color=["#1f77b4", "#2ca02c"])
    ax.set_ylabel("Net Income (£)")
    ax.set_title("Net Income Comparison")
    return fig