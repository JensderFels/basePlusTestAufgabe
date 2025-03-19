# Flask wird verwendet, um die Webanwendung zu erstellen
# render_template damit wir HTML Dateien anzeigen können
# request - holen wir uns Daten z.B. bei Eingabe eines Textes vom Benutzer
from flask import Flask, render_template, request
# PyMuPDF für die PDF-Verarbeitung
import fitz
# Modul für Datum und Uhrzeit
import datetime
# Nutze pyngrok für öffentliche URL
# from pyngrok import ngrok

# Erstelle Flask-App, __name__ benutzt, damit die richtige Datei als Hauptprogramm erkannt wird.
app = Flask(__name__)

# ngrok auskommentiert, da man hierfür einen Account sowie AuthToken benötigt, dient nur dazu, dass der Chatbot ins Internet gestellt werden könnte.

# Bewusst hier damit erst Flask startet
# public_url = ngrok.connect(5000) #Port 5000 freigeben
# Gebe die URL in der Console aus damit es leichter ist diese zu kopieren
# print(f"öffentliche URL: {public_url}")

# @app.route('/') wird aufgerufen sobald die Startseite geöffnet wird
@app.route('/')
def home():
    # zeigt die Datei index.html im Browser an
    return render_template("index.html")

# @app.route('/chat', methods=["POST"]) verwendet wenn Nachricht per POST versendet wird
@app.route('/chat', methods=["POST"])
def chat():
    # request.form holt den Text aus dem Formular
    # Für die Verarbeitung konvertiere ich den Text in Kleinbuchstaben
    user_input = request.form["message"].lower()
    # Vielleicht auch hier mit einem Dictionary arbeiten um noch mehr Wörter abzufangen aber erstmal bei den beiden Wörtern belassen
    if "uhrzeit" in user_input or "wie spät" in user_input:
        response = get_current_time()
    else:
        response = f"Gesagt wurde: {user_input}"
    return response

def get_current_time():
    # Holt das aktuelle Datum und die Uhrzeit
    now = datetime.datetime.now()
    # konvertiere now und gebe nur die Uhrzeit aus.
    return f"Die aktuelle Uhrzeit ist: {now.strftime('%H:%M:%S')}"

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