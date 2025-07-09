from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import date
import io

def generate_pdf(title: str, salary_data: dict, model: str = "Umbrella"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - inch, title)

    # Subheading
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2.0, height - inch - 20, f"Model: {model} | Date: {date.today()}")

    # Table content
    y_position = height - inch - 60
    line_height = 18
    c.setFont("Helvetica", 11)

    for label, value in salary_data.items():
        c.drawString(inch, y_position, f"{label}:")
        c.drawRightString(width - inch, y_position, f"£{value:,.2f}")
        y_position -= line_height
        if y_position < inch:
            c.showPage()
            y_position = height - inch

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
