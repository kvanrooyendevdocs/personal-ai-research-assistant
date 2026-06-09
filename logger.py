from datetime import datetime
import os
import json

from config import MODEL_NAME

def create_session_log_files():
    """
    Create one text log file and one JSON log file for the current research session.
    """
    os.makedirs("research_logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    text_filename = f"research_logs/session_{timestamp}.txt"
    json_filename = f"research_logs/session_{timestamp}.json"

    session_started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(text_filename, "w", encoding="utf-8") as file:
        file.write("Personal AI Research Assistant Session Log\n")
        file.write("==========================================\n\n")
        file.write(f"Session started: {session_started}\n")
        file.write(f"Model used: {MODEL_NAME}\n\n")

    session_data = {
        "session_started": session_started,
        "model": MODEL_NAME,
        "session_totals": {
            "total_questions": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "total_cost_usd": 0
        },
        "questions": []
    }

    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)

    return text_filename, json_filename, session_data

def update_session_totals(session_data, usage, estimated_cost):
    """
    Update the running totals for the current session.
    """
    session_data["session_totals"]["total_questions"] += 1
    session_data["session_totals"]["total_prompt_tokens"] += usage["prompt_tokens"]
    session_data["session_totals"]["total_completion_tokens"] += usage["completion_tokens"]
    session_data["session_totals"]["total_tokens"] += usage["total_tokens"]

    current_total_cost = session_data["session_totals"]["total_cost_usd"]
    new_total_cost = current_total_cost + estimated_cost["total_cost_usd"]

    session_data["session_totals"]["total_cost_usd"] = round(new_total_cost, 6)
    

def save_question_to_text_log(filename, question, answer, question_number, usage, estimated_cost):
    """
    Save one question and structured answer pair to the current text session log file.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"Question {question_number}\n")
        file.write("-" * 20)
        file.write("\n\n")

        file.write("Question:\n")
        file.write(question)
        file.write("\n\n")

        file.write("Answer:\n\n")

        file.write("Summary:\n")
        file.write(answer.get("summary", "No summary provided."))
        file.write("\n\n")

        file.write("Key points:\n")
        key_points = answer.get("key_points", [])

        if key_points:
            for point in key_points:
                file.write(f"- {point}\n")
        else:
            file.write("- No key points provided.\n")

        file.write("\nSimple explanation:\n")
        file.write(answer.get("simple_explanation", "No simple explanation provided."))
        file.write("\n\n")

        file.write("Practical example:\n")
        file.write(answer.get("practical_example", "No practical example provided."))
        file.write("\n\n")

        file.write("Usage:\n")
        file.write(f"Prompt tokens: {usage['prompt_tokens']}\n")
        file.write(f"Completion tokens: {usage['completion_tokens']}\n")
        file.write(f"Total tokens: {usage['total_tokens']}\n")
        file.write(f"Estimated cost: ${estimated_cost['total_cost_usd']}\n")

        file.write("\n")
        file.write("=" * 50)
        file.write("\n\n")
        
def save_question_to_json_log(
    filename,
    session_data,
    question,
    answer,
    question_number,
    usage,
    estimated_cost
):
    """
    Save one question and answer pair to the current JSON session log file.
    """
    question_entry = {
        "question_number": question_number,
        "question": question,
        "answer": answer,
        "model": MODEL_NAME,
        "usage": usage,
        "estimated_cost": estimated_cost,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    session_data["questions"].append(question_entry)
    update_session_totals(session_data, usage, estimated_cost)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)

