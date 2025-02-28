from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")  # Faster model

# Strict Constitution-related keywords & patterns
CONSTITUTION_KEYWORDS = [
    r"\bconstitution\b", r"\bfundamental rights\b", r"\bdirective principles\b",
    r"\bpreamble\b", r"\bpresident\b", r"\bparliament\b", r"\bsupreme court\b",
    r"\bfundamental duties\b", r"\barticle\b", r"\bschedule\b", r"\bamendment\b",
    r"\blaw\b", r"\bgovernance\b", r"\bcitizenship\b", r"\bjustice\b",
    r"\bdemocracy\b", r"\bsecularism\b", r"\bgovernment\b", r"\belections\b"
]

def is_constitution_related(question):
    """Check if the question is strictly related to the Indian Constitution."""
    question_lower = question.lower()
    return any(re.search(keyword, question_lower) for keyword in CONSTITUTION_KEYWORDS)

def get_response(question):
    """Fetch response from Gemini AI if valid, else return restriction message."""
    if is_constitution_related(question):
        try:
            response = model.generate_content(question)
            return response.text if response else "No response received."
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return "⚠️ This chatbot only answers **Constitution of India** related questions. Please ask a relevant question."

# Initialize the Streamlit app
st.set_page_config(page_title="Samvidhan Sathi 🤖", page_icon="📜")

# Set a header
st.header("Samvidhan Sathi 🤖 - Indian Constitution Chatbot")

# Display some introductory text
st.write("📜 **Ask me anything related to the Indian Constitution!** 🏛️\n🔹 *For example: What are Fundamental Rights?*\n🔹 *What does Article 21 state?*\n🚫 **Non-Constitutional questions will not be answered.**")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input box for user question
user_input = st.text_input("Ask your question about the Indian Constitution:", key="input")

# Submit button
submit = st.button("Ask the question ✨")

# Toggle chat history
show_history = st.checkbox("Show Chat History 🗨️")

# When submit is clicked
if submit and user_input:
    # Get response
    response = get_response(user_input)
    
    # Store conversation in history
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"Bot: {response}")
    
    # Display response
    st.write(response)

# Show chat history if enabled
if show_history:
    st.write("### Chat History")
    for message in st.session_state.history:
        st.write(message)
