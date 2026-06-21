from datetime import datetime


# =========================
# Chat Message Helpers
# =========================
def create_chat_message(role, content):
    """
    Create a standardized chat message object.
    """
    return {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def add_user_message(chat_history, user_question):
    """
    Add a user message to chat history.
    """
    chat_history.append(
        create_chat_message(
            role="user",
            content=user_question
        )
    )

    return chat_history


def add_assistant_message(chat_history, assistant_response):
    """
    Add an assistant message to chat history.
    """
    chat_history.append(
        create_chat_message(
            role="assistant",
            content=assistant_response
        )
    )

    return chat_history


def clear_chat_history():
    """
    Return an empty chat history.
    """
    return []


# =========================
# Chat History Formatting
# =========================
def format_chat_history_for_prompt(chat_history, max_messages=8):
    """
    Format recent chat history for the AI prompt.

    This helps the chatbot understand follow-up questions while keeping
    the context concise and controlled.
    """
    if not chat_history:
        return "No previous conversation."

    recent_messages = chat_history[-max_messages:]

    lines = []

    for message in recent_messages:
        role = message.get("role", "unknown").upper()
        content = message.get("content", "")

        lines.append(f"{role}: {content}")

    return "\n\n".join(lines)


def format_chat_history_for_markdown(chat_history):
    """
    Format full chat history for Markdown report export.
    """
    if not chat_history:
        return "No chat history available."

    lines = []

    for index, message in enumerate(chat_history, start=1):
        role = message.get("role", "unknown").title()
        timestamp = message.get("timestamp", "Unknown time")
        content = message.get("content", "")

        lines.append(f"### Message {index}: {role}")
        lines.append("")
        lines.append(f"Timestamp: {timestamp}")
        lines.append("")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)