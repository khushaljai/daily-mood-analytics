import ollama

def analyze_entry(entry_text: str) -> dict:
    """
    Sends the journal entry to Ollama (phi3) for analysis.
    Returns a dictionary with 'analysis_text' and 'mood_score'.
    """
    prompt = f"""
Analyze the following journal entry and return:
- Mood
- Stress level
- Key themes
- One insight

Please format the output cleanly. 
IMPORTANT: At the very end of your response, on a new line, output MOOD_SCORE: X
Where X is exactly 1 for Positive, 0 for Neutral, and -1 for Negative.

Entry:
{entry_text}
"""
    try:
        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.get('message', {}).get('content', '')
        
        # Parse mood score
        mood_score = 0
        lines = content.strip().split('\n')
        for line in reversed(lines):
            if "MOOD_SCORE:" in line:
                try:
                    score_str = line.split("MOOD_SCORE:")[1].strip()
                    mood_score = int(score_str)
                except ValueError:
                    mood_score = 0
                break
                
        return {
            "analysis_text": content.replace(f"MOOD_SCORE: {mood_score}", "").replace(f"MOOD_SCORE: {str(mood_score)}", "").strip(),
            "mood_score": mood_score
        }
    except Exception as e:
        return {
            "error": f"Failed to connect to Ollama: {str(e)}.\nPlease make sure Ollama is installed and running (`ollama run phi3`).",
            "analysis_text": "",
            "mood_score": 0
        }

def continue_chat(messages: list) -> str:
    """
    Sends a sequence of messages to Ollama (phi3) and returns the string response.
    messages format: [{"role": "user"|"assistant", "content": "..."}]
    """
    try:
        response = ollama.chat(
            model="phi3",
            messages=messages
        )
        return response.get('message', {}).get('content', '')
    except Exception as e:
        return f"Error: Failed to connect to Ollama: {str(e)}"
