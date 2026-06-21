import os
from dotenv import load_dotenv
from google import genai


# =========================
# Gemini Client Configuration
# =========================
def get_gemini_client():
    """
    Load Gemini API key from .env file and create a Gemini client.
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Please add it to your .env file."
        )

    return genai.Client(api_key=api_key)


def get_gemini_model():
    """
    Load Gemini model name from .env file.
    If GEMINI_MODEL is not set, use gemini-3.5-flash by default.
    """
    load_dotenv()

    return os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def generate_content(prompt):
    """
    Send a prompt to Gemini and return the generated text.
    """
    client = get_gemini_client()
    model_name = get_gemini_model()

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text


# =========================
# AI Insight Generator
# =========================
def generate_ai_insights(kpi_summary_text):
    """
    Generate business insights from structured KPI summary text.
    """
    prompt = f"""
You are a senior business analyst for a retail company.

Your task is to analyze the following structured business context and generate
clear, practical, and data-driven business insights.

Important rules:
- Use only the metrics provided in the structured context.
- Do not invent numbers.
- Do not mention data that is not available.
- Do not infer unavailable fields as zero or poor performance.
- Write in a professional business style.
- Keep the response concise and useful for managers.
- Use short paragraphs.
- Keep each bullet point under 2 lines.
- Use business-friendly language.
- Avoid combining words and numbers without spaces.
- Use clean Markdown formatting.
- Do not use markdown tables.

Structured Business Context:
{kpi_summary_text}

Please generate the response using this structure:

## Executive Summary
Summarize overall sales performance in 2-3 sentences.

## Key Business Insights
Provide 4-6 bullet points based on the structured context.

## Business Risks
Identify 2-3 potential risks or weak areas.

## Opportunities
Identify 2-3 business opportunities.

## Data-Driven Conclusion
Conclude with a short recommendation for management.
"""

    try:
        ai_response = generate_content(prompt)
        return ai_response, None

    except Exception as e:
        return None, f"Failed to generate AI insights: {e}"


# =========================
# AI Recommendation Engine
# =========================
def generate_ai_recommendations(kpi_summary_text):
    """
    Generate strategic business recommendations from structured KPI summary text.
    """
    prompt = f"""
You are a senior retail strategy consultant.

Your task is to generate practical business recommendations based only on the following structured business context.

Important rules:
- Use only the metrics provided in the structured context.
- Do not invent numbers.
- Do not mention data that is not available.
- Do not infer unavailable fields as zero or poor performance.
- Each recommendation must be actionable.
- Each recommendation must include a business reason.
- Write clearly for business managers.
- Use short paragraphs.
- Keep each bullet point under 2 lines.
- Avoid using markdown tables.
- Keep spacing clean and readable.
- Avoid combining words and numbers without spaces.
- Use clean Markdown formatting.

Structured Business Context:
{kpi_summary_text}

Please generate the response using this structure:

## Strategic Recommendations

### 1. Sales Growth
Provide 2-3 recommendations to improve revenue.

### 2. Customer Experience
Provide 2-3 recommendations to improve customer satisfaction or ratings.
If rating data is unavailable, clearly say that customer satisfaction cannot be directly evaluated from ratings.

### 3. Product and Category Strategy
Provide 2-3 recommendations related to product or category performance.

### 4. Branch and Regional Strategy
Provide 2-3 recommendations related to city, region, branch, or store performance.
If branch or region data is unavailable, clearly say so.

### 5. Priority Action Plan
List the top 3 actions management should take first.

For each recommendation, use this format:
- Action:
- Reason:
- Expected Impact:
"""

    try:
        ai_response = generate_content(prompt)
        return ai_response, None

    except Exception as e:
        return None, f"Failed to generate AI recommendations: {e}"


# =========================
# AI Business Chatbot
# =========================
def generate_chatbot_response(
    user_question,
    kpi_summary_text,
    chat_history_text=None
):
    """
    Generate an AI chatbot response based on the user's business question,
    structured KPI context, and recent chat history.
    """
    if not chat_history_text:
        chat_history_text = "No previous conversation."

    prompt = f"""
You are an AI business intelligence assistant for a retail company.

Your task is to answer the user's business question based only on:
1. The structured business context
2. The recent chat history

Important rules:
- Use only the metrics provided in the structured business context.
- Use chat history only to understand follow-up questions.
- Do not invent numbers.
- Do not mention data that is not available.
- Do not infer unavailable fields as zero or poor performance.
- If the answer cannot be determined from the structured context, clearly say that the available data is not enough.
- Write clearly and practically for business managers.
- Keep the answer concise.
- Use short paragraphs.
- Keep each bullet point under 2 lines.
- Use clean Markdown formatting.
- Avoid markdown tables.
- Avoid combining words and numbers without spaces.

Structured Business Context:
{kpi_summary_text}

Recent Chat History:
{chat_history_text}

Current User Question:
{user_question}

Please answer the question in this structure:

## Answer
Provide a direct answer to the user's question.

## Supporting Evidence
Mention the specific metrics from the structured context that support your answer.

## Business Interpretation
Explain what this means for management.
"""

    try:
        ai_response = generate_content(prompt)
        return ai_response, None

    except Exception as e:
        return None, f"Failed to generate chatbot response: {e}"