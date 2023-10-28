import streamlit as st
import openai
import requests
import json
import numpy as np
from supabase import create_client, Client

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_API_KEY"]
supabase: Client = create_client(url, key)

st.header("Lido Copilot")

st.write("""
         I'm Liddy, your Lido DAO Copilot - I'm an LLM trained on every Lido DAO proposal.
         I've reviewed all prior DAO proposals and know all relevant voting information.
         Use me to get proposal summaries, or any insights about the DAO.
         If you'd like any features in specific, contact @gigarahul on Twitter.
         """)

openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai.api_key = st.text_input("Enter API Key", type="password")

def query_proposals(): # WORKS - FIRST 1000 PROPOSALS, RETURNS JSON PROPS CLEANED 
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

def embed(docm: str): # WORKS - PASS STRING => RETURNS EMBED
    response = openai.Embedding.create(
        input=docm,
        model="text-embedding-ada-002"
        )
    emb = response['data'][0]['embedding']
    if len(emb) == 1536:
        return emb
    else:
        return st.error("Embedding is wrong size")

def update_database(): # REPLACE SUPABASE WITH NEW PROPS
    # data, count = supabase.table("lido").delete()
    props = query_proposals()
    embeds = []
    for p in props:
        str = json.dumps(p)
        id = p["id"]
        url = f"https://snapshot.org/#/lido-snapshot.eth/proposal/{id}"
        e = embed(str)
        if len(e) == 1536:
            embeds.append(e)
            data, count = supabase.table("lido").insert({"url": url, "embed": e}).execute()
        else:
            return st.error("Wrong size, update_supabase")
    return True

def search_database(question): # CALLS EMBED FROM SUPABASE
    q = embed(question)
    a = np.array(q)
    # -- works up to here


    e = supabase.table('lido').select("embed").execute()
    embeds = e.data
    # return embeds[0]['embed'] # -- len() returns 19397!?!? but the content is actually 1536 length
    final = []
    for x in embeds:
        e = np.array(x['embed'])
        return e.shape, e.dtype
        # return a
        # final.append(e)
    for f in final:
        a = np.array(q)
        b = np.array(f)
        return a.shape, a.dtype, b.shape, b.dtype
        # different shapes, sizes

        siml = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return siml
    
    # scores.append(siml)
    
    srt = sorted(scores, reverse=True)
    top = srt[:10]
    context = []
    for x in top:
        index = scores.index(x)
        context.append(index)
    return context

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
if question:
    # st.write(query_proposals())
    # st.write(search_database(question))
    # st.write(update_database())


# Goal: Talk to documentation; relevant documentation in the context window