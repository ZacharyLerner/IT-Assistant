import os
from inverted_index import query
from api_key import key
from openai import OpenAI

client = OpenAI(api_key=key)

# Extracts the keywords from a sentence to make the search more accurate
# Has functionality to detect when the user wants to change modes, and returns a special message
def extract_keywords(user_query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are an assistant that extracts important keywords from queries for optimal search results. 
             Feel free to alter keywords to make the search more optimal. Return the keywords in one spaced sentence. 
             If the users query idicated that they want to switch to ITSD mode or TLS mode respond with ITS MODE or TLS MODE respectively"""},
            {"role": "user", "content": f"Extract the important keywords from the following query: {user_query}"},
        ]
    )
    keywords = response.choices[0].message.content
    return keywords

# Uses the keywords, original proposed question, and the top results from the TF_IDF search to formulate an answer to the Question
# Had stipulations for formatting and inclusion of hyperlinks.
def query_ai(keywords, num_param, original_query, model):
    results = query(keywords, num_param,model)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are an IT Search Engine Assistant. You are a part of the URI IT Service Desk (ITSD). Respond in a conversational manner. 
         Your job is to go through the results of a query and find the most optimal answer to the proposed question, summarize it, and then return the shortened answer only. 
         Only include information from the search results. Provide links for http websites on a new line when important to the question. 
         For bulleted lists and numbered lists place each point on a new line.
         Include urls as they appear in the results, do not include any characters around them that could cause issues with the url"""},
        {"role": "user", "content": results},
        {"role": "user", "content": f"Here is the original query to find results for: {original_query}"},
    ]
    )
    return completion.choices[0].message.content