import streamlit as st
import os
import sys

# Ensure import path is correct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import Song, load_songs, AIRecommender
from src.evaluate import run_evaluation

# Page configuration
st.set_page_config(
    page_title="EchoMatch 2.0 - AI Music Discovery",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism & Sleek Dark Mode vibe)
st.markdown("""
<style>
    /* Main App Custom CSS */
    .stApp {
        background-color: #0E1117;
        color: #E2E8F0;
    }
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif;
    }
    .song-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .song-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 5px;
        color: white;
    }
    .badge-genre { background-color: #6366F1; }
    .badge-mood { background-color: #EC4899; }
    .badge-energy { background-color: #F59E0B; }
    .badge-acoustic { background-color: #10B981; }
    
    .agent-step {
        border-left: 3px solid #6366F1;
        padding-left: 15px;
        margin-bottom: 15px;
    }
    .agent-status-success { color: #10B981; font-weight: bold; }
    .agent-status-running { color: #3B82F6; font-weight: bold; }
    .agent-status-blocked { color: #EF4444; font-weight: bold; }
    .agent-status-fallback { color: #F59E0B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Helper to load songs
@st.cache_data
def get_songs():
    songs_data = load_songs("data/songs.csv")
    songs = []
    for s in songs_data:
        songs.append(
            Song(
                id=s['id'],
                title=s['title'],
                artist=s['artist'],
                genre=s['genre'],
                mood=s['mood'],
                energy=s['energy'],
                tempo_bpm=s['tempo_bpm'],
                valence=s['valence'],
                danceability=s['danceability'],
                acousticness=s['acousticness']
            )
        )
    return songs

# Initialize state
if "api_key" not in st.session_state:
    st.session_state["api_key"] = os.environ.get("GEMINI_API_KEY", "")

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=400&auto=format&fit=crop", use_container_width=True)
    st.title("Settings")
    
    # API key input
    api_key_input = st.text_input("Gemini API Key", value=st.session_state["api_key"], type="password")
    if api_key_input != st.session_state["api_key"]:
        st.session_state["api_key"] = api_key_input
        st.rerun()

    st.markdown("---")
    k_songs = st.slider("Number of Recommendations", min_value=1, max_value=10, value=3)

    st.markdown("---")
    st.subheader("System Architecture")
    st.markdown("""
    ```mermaid
    graph TD
        User([User Prompt]) --> IG[Input Guardrail]
        IG -- Blocked --> Err[Error Msg]
        IG -- Passed --> RAG[RAG Catalog Context]
        RAG --> RecAgent[Recommender Agent]
        RecAgent --> Draft[Draft Recs]
        Draft --> CritiqueAgent[Critique Agent]
        CritiqueAgent -- Issues Found --> SelfCorrect[Self Correction]
        SelfCorrect --> Final[Final Recs]
        CritiqueAgent -- Approved --> Final
        Final --> UI[Display to User]
    ```
    """, unsafe_allow_html=True)

# Main layout
st.title("🎵 EchoMatch 2.0: AI-Powered Music Discovery")
st.markdown("---")

tab1, tab2 = st.tabs(["🔎 Smart Recommendation", "🛡️ Reliability & Evaluation"])

songs = get_songs()
recommender = AIRecommender(songs, api_key=st.session_state["api_key"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("What are you in the mood for?")
        
        # Suggested prompts
        suggestion = st.selectbox(
            "Quick Suggestions:",
            [
                "Custom Query (Type below)",
                "I want some chill, relaxing acoustic music to listen to while studying.",
                "Give me intense, fast-paced rock or metal to pump me up at the gym.",
                "Something nostalgic with guitar vibes for a rainy night drive.",
                "Tell me a joke instead of recommending music."
            ]
        )

        user_input = st.text_area(
            "Enter your request in natural language:",
            value="" if suggestion == "Custom Query (Type below)" else suggestion,
            placeholder="E.g., I want some upbeat pop tracks that make me feel happy..."
        )

        search_btn = st.button("Generate Recommendations", type="primary")

        if search_btn and user_input:
            with st.spinner("Agent planning and selecting matches..."):
                try:
                    recs, logs = recommender.recommend(user_input, k=k_songs)
                    
                    st.subheader("Top Recommendations")
                    for idx, (song, reason) in enumerate(recs, 1):
                        st.markdown(f"""
                        <div class="song-card">
                            <h3>{idx}. {song.title} <span style="font-size: 1.1rem; font-weight: normal; color: #94A3B8;">by {song.artist}</span></h3>
                            <div style="margin-bottom: 12px;">
                                <span class="badge badge-genre">Genre: {song.genre}</span>
                                <span class="badge badge-mood">Mood: {song.mood}</span>
                                <span class="badge badge-energy">Energy: {song.energy:.2f}</span>
                                <span class="badge badge-acoustic">Acousticness: {song.acousticness:.2f}</span>
                            </div>
                            <p style="font-style: italic; color: #CBD5E1; margin-top: 10px;">"{reason}"</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Display Logs in Col2
                    with col2:
                        st.subheader("🤖 Agent Reasoning Logs")
                        for log in logs:
                            status_class = f"agent-status-{log['status'].lower()}"
                            st.markdown(f"""
                            <div class="agent-step">
                                <strong>{log['step']}</strong> - <span class="{status_class}">{log['status']}</span>
                                <p style="font-size: 0.9rem; color: #94A3B8; white-space: pre-wrap; margin-top: 4px;">{log['detail']}</p>
                            </div>
                            """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error executing recommendation: {e}")
                    # If we got blocked, show logs
                    if 'logs' in locals():
                        with col2:
                            st.subheader("🤖 Agent Reasoning Logs")
                            for log in logs:
                                status_class = f"agent-status-{log['status'].lower()}"
                                st.markdown(f"""
                                <div class="agent-step">
                                    <strong>{log['step']}</strong> - <span class="{status_class}">{log['status']}</span>
                                    <p style="font-size: 0.9rem; color: #94A3B8; white-space: pre-wrap; margin-top: 4px;">{log['detail']}</p>
                                </div>
                                """, unsafe_allow_html=True)

    with col2:
        if not search_btn:
            st.info("Agent reasoning and verification logs will appear here during search.")

with tab2:
    st.subheader("Guardrails & Evaluation Suite")
    st.markdown("""
    Evaluate the recommender system across four test cases (including standard and adversarial queries). 
    This triggers the guardrails, checks output formats, and evaluates for hallucinated content.
    """)

    run_eval_btn = st.button("Run Automated Evaluation")
    
    if run_eval_btn:
        with st.spinner("Running test scenarios..."):
            report = run_evaluation()
            st.markdown(report)
            st.success("Evaluation complete!")
