import streamlit as st
import openai
import requests

st.header("Lido Copilot")

"""
Everything you need to know about Lido Finance.
We've passed all prior proposals with all relevant voting information.
Use it to get proposal summaries.
Enter your personalized information to get suggestions.
Talk to Lido proposals.
"""

# Collect All Lido Proposals in SQL
# Query GraphQL For Lido Info
# Put 
# Embed SQL into 
# Embed All Lido Proposals
# Pass the embedding into the chat completion and 

# User Enters Question in Text Input,
# User Presses Button
# Button Triggers API Call
# API Call Returns Text Answer
# Answer Is Displayed With st.write
# Embed all proposals
# Chat with embedding

def query_proposals():
    url = "https://hub.snapshot.org/graphql"
    query = """
    query {
        proposals (
            first: 1000000
            skip: 0,
            where: {
                space_in: ["lido-snapshot.eth"],
                },
                orderBy: "created",
                orderDirection: asc
                ) {
                    id
                    title
                    body
                    choices
                    start
                    end    
                    snapshot
                    state
                    scores
                    scores_by_strategy
                    scores_total
                    scores_updated
                    author
                    space {
                        id
                        name
                        }
                        }
                        }
                        """
    data = {'query': query}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.write('Request failed with status code', response.status_code)

def embed_docm(docm):
    # embed each proposal as its own document
    # create a 
    return embeds

def similarity_search(question, embeds):
    # embed question
    # similarity search for 
    return docm

def talk_to_proposals():

    return response

openai.api_key = st.text_input("OpenAI API Key", type="password")
question = st.text_input("Talk to Lido proposals")

query_proposals()