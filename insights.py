import ollama

def generate_weekly_reflection(entries_df) -> str:
    """
    Receives recent entries DataFrame and uses Ollama to generate a weekly insight.
    """
    if entries_df.empty:
        return "Not enough data to generate a weekly reflection. Keep journaling!"
    
    entries_text = ""
    for _, row in entries_df.iterrows():
        entries_text += f"Date: {row['date']}\nEntry: {row['entry']}\n\n"
        
    prompt = f"""
Based on the following journal entries from the past week, generate a weekly reflection.
The reflection should include:
- Mood Trend
- Recurring Themes
- Positive Patterns
- Advice for Improvement

Provide the output cleanly formatted.

Here are the entries:
{entries_text}
"""
    try:
        response = ollama.chat(
            model="phi3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.get('message', {}).get('content', "Failed to generate reflection.")
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}.\nPlease ensure Ollama is installed and running with `ollama run phi3`."
