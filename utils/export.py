import io
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from utils.charts import plot_income_pie, plot_net_income_bar


def export_to_csv(data: dict, model: str) -> bytes:
    df = pd.DataFrame(data.items(), columns=["Field", "Value"])
    return df.to_csv(index=False).encode("utf-8")


def export_to_pdf(umbrella_data: dict, ltd_data: dict) -> bytes:
    buffer = io.BytesIO()
    with PdfPages(buffer) as pdf:
        # Umbrella Chart
        fig1 = plot_income_pie(umbrella_data, "Umbrella")
        pdf.savefig(fig1)
        plt.close(fig1)

        # Ltd Chart
        fig2 = plot_income_pie(ltd_data, "Ltd")
        pdf.savefig(fig2)
        plt.close(fig2)

        # Comparison Chart
        fig3 = plot_net_income_bar(umbrella_data, ltd_data)
        pdf.savefig(fig3)
        plt.close(fig3)

    buffer.seek(0)
    return buffer.read()