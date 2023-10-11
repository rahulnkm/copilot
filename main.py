import streamlit as st
import openai
import requests
import json

st.header("Lido Copilot")

st.write("""
         I'm Liddy, your Lido DAO Copilot - I know everything there is to know about Lido DAO.
         I've reviewed all prior DAO proposals and know all relevant voting information.
         Use me to get proposal summaries, or any insights about the DAO.
         If you'd like any features in specific, contact @gigarahul on Twitter.
""")

openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai.api_key = st.text_input("Enter API Key", type="password")

# User Enters Question in Text Input,
# User Presses Button
# Button Triggers API Call
# API Call Returns Text Answer
# Answer Is Displayed With st.write
# Embed all proposals
# Chat with embedding

def query_proposals(): # WORKS - FIRST 1000 PROPOSALS, RETURNS CLEANED JSON
    url = "https://hub.snapshot.org/graphql"
    query = """
    query {
        proposals (
            first: 1000
            skip: 0,
            where: {
                space_in: ["lido-snapshot.eth"],
                },
                orderBy: "created",
                orderDirection: desc
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
        json = response.json()
        return json["data"]["proposals"]
    else:
        st.error('Request failed with status code', response.status_code)

def embed_docm(docm): # WORKS - PASS STRING => EMBEDS ANY STRING
    response = openai.Embedding.create(
        input=docm,
        model="text-embedding-ada-002"
        )
    emb = response['data'][0]['embedding']
    return emb

def create_index(props): # WORKS - PASS PROPS => CREATES ARRAY OF PROP EMBEDS
    embeds = []
    for p in props:
        str = json.dumps(p)
        e = embed_docm(str)
        embeds.append(e)
    return embeds

def similarity_search(question, embeds):
    q = embed_docm(question)
    sorted = []
    for x in embeds:

        sorted.append(x)
        # compare q to each
        # move highest similarity to front
    return sorted[:10]

def talk_to_proposals(ctx, question):
    system_prompt = """
    You are a professional business assistant for Lido DAO investors and stakeholders. Answer questions accurately and concisely and with a friendly cadence.
    """
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": ctx[0]},
            {"role": "system", "content": ctx[1]},
            {"role": "system", "content": ctx[2]},
            {"role": "system", "content": ctx[3]},
            {"role": "system", "content": ctx[4]},
            {"role": "system", "content": ctx[5]},
            {"role": "system", "content": ctx[6]},
            {"role": "system", "content": ctx[7]},
            {"role": "system", "content": ctx[8]},
            {"role": "system", "content": ctx[9]},
            {"role": "user", "content": question},
            ]
            )
    return result['choices'][0]['message']['content']

question = st.text_input("Talk to Lido proposals")

if st.button("Go"):
    st.write(create_index(query_proposals()))