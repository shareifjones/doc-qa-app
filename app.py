# gives you access to your operating system, specifically we need it to read environment variables (like your API key from the .env file)
import os
# imports the tool that reads your .env file
from dotenv import load_dotenv
# imports the Anthropic library so we can talk to Claude
import anthropic

# reads the .env file and loads everything in it into memory
load_dotenv()

# creates a connection to Anthropic's API, authenticated with your key, and stores it in a variable called client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_question(document, question):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        # limits how long the response can be. A token is roughly one word. 1024 tokens means Claude won't write you an essay when you just need a short answer.
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Here is a document:\n\n{document}\n\nAnswer this question based on the document: {question}"
            }
        ]
    )
    # gets the text of Claude's response back out.
    return message.content[0].text

file_path = input("Enter the path to your text file: ")

# open(file_path, "r") opens the file at that path — the "r" means read-only
# with is a clean way to open files — it automatically closes the file when you're done with it, even if something goes wrong
with open (file_path, "r") as f:
    # f.read() reads the entire contents of the file into the document variable
    document = f.read()

question = input("What would you like to know about this document? ")


answer = ask_question(document, question)
print("\nAnswer: ", answer)