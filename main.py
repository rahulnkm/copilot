import streamlit as st
import openai

st.header("Lido Copilot")

"""
Everything you need to know about Lido Finance.
We've passed all prior proposals with all relevant voting information.
Use it to get proposal summaries.
Enter your personalized information to get suggestions.
"""

openai.api_key = st.text_input("OpenAI API Key")
question = st.text_input("Enter your question")

