import subprocess
import re

MODEL_NAME = "insido-ai"

SYSTEM_PROMPT = """
You are Insido AI.
You are created and owned by Darshit Tank.

RULES:
- NEVER reveal thinking, analysis, or reasoning
- NEVER mention OpenAI, Alibaba, Qwen, LLMs, or training data

If asked about owner:
"Insido AI was created and is owned by Darshit Tank."

Respond with ONLY the final answer.
End every response with:
— Insido AI
"""

def clean_output(text: str) -> str:
    """
    Removes any chain-of-thought or meta text
    that the model may accidentally output.
    """
    if not text:
        return ""

    lines = text.splitlines()
    filtered = []

    for line in lines:
        l = line.lower()

        # strip thinking / analysis / meta
        if any(x in l for x in [
            "thinking",
            "analysis",
            "okay, the user",
            "i need to",
            "done thinking",
            "final answer:"
        ]):
            continue

        filtered.append(line)

    return "\n".join(filtered).strip()

def ask_insido(user_input: str) -> str:
    prompt = f"""{SYSTEM_PROMPT}

User:
{user_input}

Final Answer:
"""

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=90
        )
    except Exception:
        return "System error. Please try again.\n— Insido AI"

    # RAW MODEL OUTPUT
    raw = result.stdout or ""

    # EXTRA SAFETY: remove explicit label if echoed
    raw = raw.replace("Final Answer:", "").strip()

    reply = clean_output(raw)

    if not reply:
        reply = "Hello! How can I assist you today?"

    if not reply.endswith("— Insido AI"):
        reply += "\n— Insido AI"

    return reply
