from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import os

# Load variables from the .env file
load_dotenv()

# Create the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ask the user for a question
question = input("Ask your research question: ").strip()

# Check that the user actually typed something
if not question:
    print("Please enter a question before running the assistant.")
    exit()

try:
    # Send the question to the AI model
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful research assistant.

When answering, always use this structure:

Summary:
Give a short 2-3 sentence summary.

Key points:
- Give the most important points as bullet points.

Simple explanation:
Explain the idea in beginner-friendly language.

Practical example:
Give one practical example of how this could be used.
""",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    # Get the AI's answer
    answer = response.choices[0].message.content

    # Print the AI's answer
    print("\nAI Answer:\n")
    print(answer)

    # Create the research_logs folder if it does not already exist
    os.makedirs("research_logs", exist_ok=True)

    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the filename
    filename = f"research_logs/research_{timestamp}.txt"

    # Save the question and answer to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Research Assistant Log\n")
        file.write("======================\n\n")
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write("Question:\n")
        file.write(question)
        file.write("\n\nAnswer:\n")
        file.write(answer)

    print(f"\nResearch saved to: {filename}")

except Exception as error:
    print("\nSomething went wrong while contacting the AI model.")
    print("Error details:")
    print(error)