import matplotlib.pyplot as plt

def create_pie_chart(data: dict, labels: list[str]):
    values = [data.get(label, 0) for label in labels]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

def create_bar_chart(categories: list[str], values: list[float], title=""):
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=["#8888ff", "#44cc44", "#ffaa00"])
    ax.set_ylabel("£ per Year")
    ax.set_title(title)
    return fig
