from dotenv import load_dotenv
from openai import OpenAI
import os
import json

from config import MODEL_NAME, SYSTEM_PROMPT

def load_client():
    """
    Load the OpenAI API key from the .env file
    and create an OpenAI client.
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

    return OpenAI(api_key=api_key)

def get_ai_answer(client, question):
    """
    Send the user's question to the AI model and return a structured answer plus token usage.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    raw_answer = response.choices[0].message.content

    try:
        structured_answer = json.loads(raw_answer)
    except json.JSONDecodeError:
        structured_answer = {
            "summary": "The model returned an answer, but it was not valid JSON.",
            "key_points": [],
            "simple_explanation": raw_answer,
            "practical_example": "No structured practical example was provided."
        }

    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

    return structured_answer, usage
