# Smart AI Journal (Local LLM)

A privacy-focused, 100% local journaling application that uses AI to analyze your daily entries, track your mood, and provide weekly insights. Your data never leaves your machine!

Powered by [Streamlit](https://streamlit.io/) and [Ollama](https://ollama.com/) (running the locally-hosted `phi3` model).

## Features

- **Daily Journaling**: Write entries in a clean, distraction-free UI.
- **AI Analysis**: Get instant feedback on your mood, stress levels, key themes, and daily insights.
- **Mood Tracking**: Visualize your emotional well-being over time with automated charts.
- **Weekly Reflections**: Generate an AI-powered summary of your past 7 days, highlighting recurring themes and offering actionable advice.
- **100% Local**: Uses SQLite for storage and Ollama for AI. Complete privacy, no external APIs.

## Prerequisites

1. Python 3.11+
2. [Ollama](https://ollama.com/download) installed on your system.

## Setup Instructions

1. **Clone or download this repository**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Download the Phi-3 model via Ollama:**
   ```bash
   ollama pull phi3
   ```
4. **Ensure the Ollama service is running:**
   ```bash
   # In a new terminal tab, start the model
   ollama run phi3
   ```
5. **Run the Streamlit application:**
   ```bash
   # Run this inside the smart_ai_journal folder
   streamlit run app.py
   ```

The app will start and open in your default browser at `http://localhost:8501`.

## Structure

- `app.py`: Main Streamlit UI.
- `database.py`: Handles SQLite setup and interactions.
- `ai_analysis.py`: Connects to Ollama for entry analysis.
- `insights.py`: Generates the weekly reflections.
- `visualization.py`: Renders Matplotlib charts.
- `data/journal.db`: Your local SQLite database (created automatically).
