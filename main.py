import streamlit as st
import openai
import requests
import json

st.header("Lido Copilot")

st.write("""
Everything you need to know about Lido Finance.
We've passed all prior proposals with all relevant voting information.
Use it to get proposal summaries.
Enter your personalized information to get suggestions.
Talk to Lido proposals.
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
        # compare q to each
        # move highest similarity to front
        return sorted

def talk_to_proposals(context, question):
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt}, # Bot is representative
            {"role": "user", "content": question}
            ]
            )
    return result['choices'][0]['message']['content']

question = st.text_input("Talk to Lido proposals")

if st.button("Go"):
    # st.write(embed_docm("sup g"))
    st.write(create_index(query_proposals()))
    st.write(query_proposals())