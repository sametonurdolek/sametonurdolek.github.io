from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create-pdf-images", methods=["POST"])
def create_pdf_images():
    try:
        images = request.files.getlist("images")

        if len(images) != 4:
            return "Lütfen tam 4 görsel yükleyin.", 400

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        # Her görseli 90x120 boyutuyla 2x2 yerleştir
        positions = [(10, 10), (110, 10), (10, 150), (110, 150)]

        for i, image_file in enumerate(images):
            img = Image.open(image_file)
            img = img.convert("RGB")

            # JPEG olarak byte stream'e kaydet
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)

            x, y = positions[i]
            pdf.image(buffer, x=x, y=y, w=90, h=120)

        # PDF’i response olarak döndür
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            download_name="gorsel_pdf.pdf",
            as_attachment=True,
            mimetype="application/pdf"
        )

    except Exception as e:
        return f"Hata: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
