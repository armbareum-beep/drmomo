from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Veterinary Emergency Guide (Dummy Data)")

    # Content
    c.setFont("Helvetica", 12)
    text_lines = [
        " ",
        "1. Vomiting in Dogs:",
        "   - If a dog vomits once but is otherwise acting normal, withhold food for 12 hours.",
        "   - Offer small amounts of water frequently.",
        "   - If vomiting persists or contains blood, seek immediate veterinary attention.",
        "   - Warning: Do not induce vomiting unless instructed by a vet.",
        " ",
        "2. Chocolate Toxicity:",
        "   - Chocolate contains theobromine, which is toxic to dogs.",
        "   - Symptoms include vomiting, diarrhea, rapid breathing, and seizures.",
        "   - Dark chocolate and baking chocolate are more dangerous than milk chocolate.",
        "   - Immediate veterinary treatment is required if ingestion is suspected.",
        " ",
        "3. Heatstroke:",
        "   - Signs: Excessive panting, drooling, red gums, lethargy.",
        "   - Action: Move to a cool area, wet with cool (not cold) water.",
        "   - Do not use ice water as it can constrict blood vessels.",
        "   - Transport to a vet immediately.",
        " ",
        "4. Seizures:",
        "   - Do not put your hands in the dog's mouth.",
        "   - Move objects away to prevent injury.",
        "   - Note the time and duration of the seizure.",
        "   - If it lasts more than 5 minutes, it is an emergency.",
    ]

    y = height - 100
    for line in text_lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()
    print(f"Created dummy PDF: {filename}")

if __name__ == "__main__":
    create_dummy_pdf("veterinary_guide.pdf")
