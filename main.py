import os
from datetime import datetime
from database import (
    create_database,
    save_question_to_database,
    get_recent_questions
)
from config import (
    MODEL_NAME,
    INPUT_COST_PER_1M_TOKENS,
    OUTPUT_COST_PER_1M_TOKENS
)
from logger import (
    create_session_log_files,
    save_question_to_text_log,
    save_question_to_json_log
)

from ai_service import load_client, get_ai_answer



def print_welcome_message(text_log_file, json_log_file):
    """
    Print the welcome message and available commands.
    """
    print("Personal AI Research Assistant")
    print("==============================")
    print(f"Model: {MODEL_NAME}")
    print("\nType a research question to get started.")
    print("Type 'help' to view available commands.")
    print(f"\nText session log created: {text_log_file}")
    print(f"JSON session log created: {json_log_file}")
    print("Type 'history' to view recent saved database questions.")


def print_help():
    """
    Print available CLI commands.
    """
    print("\nAvailable commands:")
    print("help     - Show this help menu")
    print("summary  - Show current session totals")
    print("last     - Show the last question and answer")
    print("clear    - Clear the terminal screen")
    print("exit     - Save and quit the program")


def get_user_question():
    """
    Ask the user for a research question or command.
    """
    question = input("\nAsk your research question, or type a command: ").strip()
    return question



def calculate_estimated_cost(usage):
    """
    Estimate the API cost based on token usage.

    Costs are calculated using a simple per-1-million-token rate.
    """
    input_tokens = usage["prompt_tokens"]
    output_tokens = usage["completion_tokens"]

    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M_TOKENS
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M_TOKENS

    total_cost = input_cost + output_cost

    return {
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6)
    }





def print_session_summary(session_data):
    """
    Print the current session totals in a readable format.
    """
    totals = session_data["session_totals"]

    print("\nSession summary:")
    print(f"Questions asked: {totals['total_questions']}")
    print(f"Prompt tokens used: {totals['total_prompt_tokens']}")
    print(f"Completion tokens used: {totals['total_completion_tokens']}")
    print(f"Total tokens used: {totals['total_tokens']}")
    print(f"Estimated total cost: ${totals['total_cost_usd']}")


def print_last_question(session_data):
    """
    Print the most recent question and answer from the current session.
    """
    questions = session_data["questions"]

    if not questions:
        print("\nNo questions have been asked yet.")
        return

    last_entry = questions[-1]

    print("\nLast question:")
    print(last_entry["question"])

    print("\nLast answer:")
    print(last_entry["answer"])

    print("\nUsage:")
    print(f"Tokens used: {last_entry['usage']['total_tokens']}")
    print(f"Estimated cost: ${last_entry['estimated_cost']['total_cost_usd']}")


def clear_screen():
    """
    Clear the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")


def handle_command(command, session_data):
    """
    Handle built-in CLI commands.

    Returns True if a command was handled.
    Returns False if the input should be treated as a normal question.
    """
    command = command.lower()

    if command == "help":
        print_help()
        return True

    if command == "summary":
        print_session_summary(session_data)
        return True

    if command == "last":
        print_last_question(session_data)
        return True

    if command == "clear":
        clear_screen()
        return True

    return False

def print_structured_answer(answer):
    """
    Print the structured AI answer in a readable format.
    """
    print("\nAI Answer:\n")

    print("Summary:")
    print(answer.get("summary", "No summary provided."))

    print("\nKey points:")
    key_points = answer.get("key_points", [])

    if key_points:
        for point in key_points:
            print(f"- {point}")
    else:
        print("- No key points provided.")

    print("\nSimple explanation:")
    print(answer.get("simple_explanation", "No simple explanation provided."))

    print("\nPractical example:")
    print(answer.get("practical_example", "No practical example provided."))
    
def print_database_history(limit=5):
    """
    Print the most recent saved questions from the database.
    """
    recent_questions = get_recent_questions(limit)

    if not recent_questions:
        print("\nNo database history found yet.")
        return

    print(f"\nRecent database history: Last {len(recent_questions)} question(s)")

    for row in recent_questions:
        question_id, question, total_tokens, estimated_cost_usd, created_at = row

        print(f"\n{question_id}. {question}")
        print(f"   Tokens: {total_tokens}")
        print(f"   Cost: ${estimated_cost_usd}")
        print(f"   Date: {created_at}")
        
        
def main():
    """
    Main program flow.
    """
    try:
        client = load_client()
        create_database()
        text_log_file, json_log_file, session_data = create_session_log_files()
        question_count = 0

        print_welcome_message(text_log_file, json_log_file)

        while True:
            user_input = get_user_question()

            if user_input.lower() == "exit":
                print("\nGoodbye!")
                print(f"Text session saved to: {text_log_file}")
                print(f"JSON session saved to: {json_log_file}")
                print_session_summary(session_data)
                break
            if user_input.lower() == "history":
                print_database_history()
                continue
            if user_input.lower() == "summary":
                print_session_summary(session_data)
                continue
            if not user_input:
                print("Please enter a question or command.")
                continue

            if handle_command(user_input, session_data):
                continue

            question_count += 1

            print("\nThinking...")

            answer, usage = get_ai_answer(client, user_input)
            estimated_cost = calculate_estimated_cost(usage)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print_structured_answer(answer)
            print(answer)

            save_question_to_text_log(
                text_log_file,
                user_input,
                answer,
                question_count,
                usage,
                estimated_cost
            )

            save_question_to_json_log(
                json_log_file,
                session_data,
                user_input,
                answer,
                question_count,
                usage,
                estimated_cost
            )
            save_question_to_database(
                user_input,
                answer,
                MODEL_NAME,
                usage,
                estimated_cost,
                timestamp
            )

            print(f"\nQuestion {question_count} saved to text log, JSON log, and database.")
            print(f"Tokens used: {usage['total_tokens']}")
            print(f"Estimated cost: ${estimated_cost['total_cost_usd']}")

    except KeyboardInterrupt:
        print("\n\nProgram stopped by user.")

    except Exception as error:
        print("\nSomething went wrong.")
        print("Error details:")
        print(error)


if __name__ == "__main__":
    main()