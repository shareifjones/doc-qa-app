from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import anthropic
import markdown

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
    # converts the file from raw bytes into readable text
    document = file.read().decode("utf-8")

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