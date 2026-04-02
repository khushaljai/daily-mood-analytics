import streamlit as st
import database as db
import ai_analysis as ai
import insights
import visualization as viz

# Ensure database is initialized
db.init_db()

st.set_page_config(page_title="Smart AI Journal", page_icon="📖", layout="wide")

# Sidebar styling
st.sidebar.title("📖 Smart AI Journal")
st.sidebar.markdown("Your private, local AI companion.")

page = st.sidebar.radio(
    "Navigation", 
    ["Write Entry", "View Past Entries", "Chat with Journal", "Mood Analytics", "Weekly Reflection"]
)

st.sidebar.markdown("---")
st.sidebar.info("Data is stored locally in `journal.db`.\nAI runs locally via Ollama.")

if page == "Write Entry":
    st.title("📝 Write Journal Entry")
    st.write("How was your day? Pour your thoughts into your private journal.")
    
    from autocorrect import Speller
    spell = Speller(lang='en')

    def autocorrect_entry():
        if "entry_text" in st.session_state and st.session_state.entry_text.strip():
            st.session_state.entry_text = spell(st.session_state.entry_text)

    entry_text = st.text_area("Your Entry", height=250, placeholder="Today I felt...", key="entry_text")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("Spell Check & Auto Correct", on_click=autocorrect_entry)
                
    with col2:
        if st.button("Analyze and Save", type="primary"):
            if entry_text.strip():
                with st.spinner("Analyzing with Phi-3 via Ollama..."):
                    result = ai.analyze_entry(entry_text)
                    
                    if "error" in result and result["error"]:
                        st.error(result["error"])
                    else:
                        analysis_text = result["analysis_text"]
                        mood_score = result["mood_score"]
                        
                        # Store in database
                        db.add_entry(entry_text, analysis_text, mood_score)
                        
                        st.success("Entry saved successfully!")
                        
                        st.subheader("🤖 AI Analysis")
                        st.markdown(analysis_text)
                        
                        # Display simple mood indicator
                        mood_str = "Positive 😊" if mood_score == 1 else "Neutral 😐" if mood_score == 0 else "Negative 😔"
                        st.info(f"Detected Mood: **{mood_str}**")
            else:
                st.warning("Please write something before saving.")

elif page == "View Past Entries":
    st.title("📚 Past Entries")
    st.write("Review your previous thoughts and AI insights.")
    
    df = db.get_all_entries()
    
    if df.empty:
        st.info("No entries found. Start journaling to see your past entries here.")
    else:
        for _, row in df.iterrows():
            mood_indicator = "🟢" if row['mood_score'] == 1 else "🟡" if row['mood_score'] == 0 else "🔴"
            with st.expander(f"{row['date']} | {mood_indicator} Mood Score: {row['mood_score']}"):
                st.markdown("### Your Entry")
                st.write(row['entry'])
                st.markdown("---")
                st.markdown("### AI Analysis")
                st.markdown(row['analysis'])

elif page == "Chat with Journal":
    st.title("💬 Chat with your Journal")
    st.write("Talk to your AI companion about your past entries, thoughts, and reflections.")

    if "chat_messages" not in st.session_state:
        # Pre-seed the chat with some context about the user's journal
        system_prompt = "You are a helpful, empathetic AI companion. The user has a journal where they write their daily thoughts. You are chatting with them to reflect on their feelings, provide insights, and be a supportive listener."
        st.session_state.chat_messages = [{"role": "system", "content": system_prompt}]

    # Display chat messages (skipping the system prompt so the user doesn't see it)
    for msg in st.session_state.chat_messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to state and display it
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Phi-3 is typing..."):
                response = ai.continue_chat(st.session_state.chat_messages)
                st.markdown(response)
                
        # Add assistant message to history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})

elif page == "Mood Analytics":
    st.title("📊 Mood Analytics")
    st.write("Visualize your emotional journey over time.")
    
    df = db.get_all_entries()
    
    if df.empty:
        st.info("No data available for analytics. Start journaling to see your trends.")
    else:
        st.subheader("Your Mood Trend")
        fig = viz.plot_mood_trend(df)
        st.pyplot(fig)
        
        # summary stats
        st.subheader("Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Entries", len(df))
        with col2:
            avg_mood = df['mood_score'].mean()
            label = "Positive" if avg_mood > 0.3 else "Negative" if avg_mood < -0.3 else "Neutral"
            st.metric("Average Mood", f"{label} ({avg_mood:.2f})")
        with col3:
            recent_df = db.get_recent_entries(7)
            st.metric("Entries (Last 7 Days)", len(recent_df))

elif page == "Weekly Reflection":
    st.title("🌟 Weekly AI Reflection")
    st.write("Get a summary of your week, recurring themes, and customized advice.")
    
    if st.button("Generate Reflection", type="primary"):
        with st.spinner("Reflecting on your past 7 days with Phi-3..."):
            recent_df = db.get_recent_entries(days=7)
            if recent_df.empty:
                st.info("No entries from the past 7 days. Add some entries first to get a reflection!")
            else:
                reflection = insights.generate_weekly_reflection(recent_df)
                st.markdown("---")
                st.markdown("### 🤖 Your AI Weekly Reflection")
                st.markdown(reflection)
