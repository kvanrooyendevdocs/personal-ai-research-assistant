# Personal AI Research Assistant CLI

A Python command-line research assistant that uses the OpenAI API to answer user questions in a clear, structured format and save each question-and-answer session to a local research log file.

This is the first stage of a larger AI Engineering portfolio project. The long-term goal is to evolve this into a full AI-powered document assistant with a backend API, database, RAG, monitoring, and deployment.

---

## Features

- Ask research questions from the command line
- Send questions to an OpenAI model
- Receive structured AI answers
- Save each question and answer to a timestamped text file
- Store API keys safely using a `.env` file
- Basic input validation
- Basic error handling for failed API calls
- GitHub-safe setup using `.gitignore`

---

## Example Output

```text
Ask your research question: What is RAG in AI engineering?

AI Answer:

Summary:
RAG stands for Retrieval-Augmented Generation...

Key points:
- RAG combines retrieval and generation.
- It allows an AI model to use external documents.
- It helps reduce hallucinations.

Simple explanation:
Imagine asking a question and first checking your notes before answering...

Practical example:
A school policy assistant could search uploaded school documents before answering a parent's question.
Tech Stack
Python
OpenAI API
python-dotenv
Git and GitHub
Project Structure
personal-ai-research-assistant/
│
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── research_logs/        # Ignored by Git
Setup Instructions
1. Clone the repository
git clone https://github.com/kvanrooyendevdocs/personal-ai-research-assistant.git
cd personal-ai-research-assistant
2. Create a virtual environment
py -m venv .venv
3. Activate the virtual environment

For PowerShell:

.venv\Scripts\Activate.ps1

For Command Prompt:

.venv\Scripts\activate.bat
4. Install dependencies
pip install -r requirements.txt
5. Create a .env file

Create a file called .env in the project root.

Inside it, add:

OPENAI_API_KEY=your_openai_api_key_here

Do not upload your .env file to GitHub.

How to Run

Run the program with:

.venv\Scripts\python.exe main.py

Then type a research question when prompted.

Example:

Ask your research question: Explain APIs simply
How It Works

The program:

Loads the OpenAI API key from the .env file.
Asks the user to enter a research question.
Checks that the question is not empty.
Sends the question to the OpenAI API.
Requests a structured answer using a system prompt.
Prints the answer in the terminal.
Saves the question and answer to a timestamped file in research_logs.
What I Learned

This project demonstrates beginner AI Engineering skills, including:

Using environment variables for API keys
Calling an AI API from Python
Structuring prompts for consistent output
Handling user input
Writing results to files
Using Git and GitHub safely
Ignoring sensitive files with .gitignore
Future Improvements

Planned improvements include:

Refactor the code into functions
Add a loop so users can ask multiple questions in one session
Save logs as JSON instead of only text
Add SQLite database storage
Build a FastAPI backend
Add document upload
Add RAG with embeddings and vector search
Add source-cited answers
Deploy as a portfolio web app
Roadmap

This project is Stage 1 of a larger AI Engineering roadmap.

Stage 1: Python CLI Assistant

Current stage.

Python
OpenAI API
.env secrets
structured AI responses
research logs
Stage 2: Backend API

Planned.

FastAPI
Pydantic
SQLite/PostgreSQL
API endpoints
authentication basics
Stage 3: RAG Document Assistant

Planned.

PDF upload
text chunking
embeddings
vector search
document-based answers
source citations
Stage 4: Production AI System

Planned.

logging
monitoring
cost tracking
prompt injection protection
output validation
testing
Stage 5: Deployment and Portfolio

Planned.

Docker
GitHub Actions
cloud deployment
README screenshots
demo video
live portfolio app
Author

Built by Keenan Van Rooyen as part of an AI Engineering learning and portfolio pathway.