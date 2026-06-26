from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import anthropic
import markdown
from docx import Document
import pdfplumber
import io

load_dotenv()

# creates your web app. Think of this like the equivalent of client for Anthropic — it's the main object everything runs through
app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# this is a decorator. It tells Flask "when someone visits the homepage (/), run the function below"
@app.route("/")
# the function that runs when someone hits that route
def index():
    # sends the HTML page back to the browser
    return render_template("index.html")

# methods=["POST"] — this route only accepts form submissions, not regular page visits
@app.route("/ask", methods=["POST"])
def ask():
    # grabs the uploaded file from the form
    file = request.files["document"]
    # grabs the typed question from the form
    question = request.form["question"]

    filename = file.filename.lower()
    file_bytes = file.read()

    if filename.endswith(".txt"):
        document = file_bytes.decode("utf-8")
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        document = "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            document = "\n".join([page.extract_text() or "" for page in pdf.pages])
    else:
        return render_template("index.html", answer="Unsupported file type. Please upload a .txt, .docx, or .pdf file.")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Here is a document:\n\n{document}\n\nAnswer this question based on the document: {question}"
            }
        ]
    )
    # gets the text of Claude's response back out.
    answer = markdown.markdown(message.content[0].text)
    # sends the answer back to the page to display
    return render_template("index.html", answer=answer)

# This starts the web server when you run the file. debug=True means it'll auto-reload when you make changes.
if __name__ == "__main__":
    app.run(debug=True)