import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import qrcode
import io
import pandas as pd

# Card size (standard ID card)
CARD_WIDTH = 85.6 * mm
CARD_HEIGHT = 54 * mm

def generate_qr(data):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def create_voter_card(voter_id, name, father, gender, dob, output="voter_card.pdf"):
    c = canvas.Canvas(output, pagesize=(CARD_WIDTH, CARD_HEIGHT))

    # Background
    c.setFillColor(colors.whitesmoke)
    c.rect(0, 0, CARD_WIDTH, CARD_HEIGHT, fill=1, stroke=1)

    # Title
    c.setFillColor(colors.HexColor("#003366"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(CARD_WIDTH / 2, CARD_HEIGHT - 6 * mm, "ELECTION COMMISSION OF INDIA")

    # Voter details
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawString(5 * mm, 35 * mm, f"Name: {name}")
    c.drawString(5 * mm, 30 * mm, f"Father's Name: {father}")
    c.drawString(5 * mm, 25 * mm, f"Gender: {gender}")
    c.drawString(5 * mm, 20 * mm, f"DOB: {dob}")
    c.drawString(5 * mm, 15 * mm, f"Voter ID: {voter_id}")

    # QR Code
    qr_buf = generate_qr(voter_id)
    c.drawImage(ImageReader(qr_buf), CARD_WIDTH - 20 * mm, 5 * mm, 15 * mm, 15 * mm)

    c.save()
    print(f"✅ Voter card created: {output}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python voter_card_generation.py <VoterID>")
        sys.exit(1)

    voter_id_input = sys.argv[1]  # Voter ID from command line

    # Load CSV (make sure path is correct)
    df = pd.read_csv("Data\\Voter_Card.csv")

    # Search for Voter ID
    voter = df[df["Voter ID"] == voter_id_input]

    if voter.empty:
        print(f"❌ Voter ID {voter_id_input} not found in CSV.")
        sys.exit(1)

    # Extract details
    row = voter.iloc[0]
    create_voter_card(
        voter_id=row["Voter ID"],
        name=row["Name"],
        father=row["Father's Name / Husband's Name"],
        gender=row["Gender"],
        dob=row["DOB"],
        output=f"{row['Voter ID']}_card.pdf"
    )