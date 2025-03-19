# Flask wird verwendet, um die Webanwendung zu erstellen
# render_template damit wir HTML Dateien anzeigen können
# request - holen wir uns Daten z.B. bei Eingabe eines Textes vom Benutzer
from flask import Flask, render_template, request
# PyMuPDF für die PDF-Verarbeitung
import fitz

# Erstelle Flask-App, __name__ benutzt, damit die richtige Datei als Hauptprogramm erkannt wird.
app = Flask(__name__)

# @app.route('/') wird aufgerufen sobald die Startseite geöffnet wird
@app.route('/')
def home():
    # zeigt die Datei index.html im Browser an
    return render_template("index.html")

# @app.route('/chat', methods=["POST"]) verwendet wenn Nachricht per POST versendet wird
@app.route('/chat', methods=["POST"])
def chat():
    # request.form holt den Text aus dem Formular
    user_input = request.form["message"]
    # Mache es hier simpel und gebe das gefragte wieder aus, hier könnte man z.B. ein Dictionary verwenden und anhand KEY Wörter antworten.
    response = f"Gesagt wurde: {user_input}"
    return response

# Neue Route /upload
@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return "Keine Datei hochgeladen!", 400

    pdf_file = request.files["pdf"]

    if pdf_file.filename == "":
        return "Ungültige Datei!", 400

    text = extract_text_from_pdf(pdf_file)
    return text if text else "Fehler beim Verarbeiten der Datei!"

# Liest Text von der PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Main-Methode
if __name__ == "__main__":
    app.run(debug=True)