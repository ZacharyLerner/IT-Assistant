import os
from inverted_index import query
from api_key import key
from openai import OpenAI

client = OpenAI(api_key=key)


def extract_keywords(user_query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts important keywords from queries for optimal search results. Feel free to alter keywords to make the search more optimal. Return the keywords in one spaced sentence. If the user ever says anything that indicates they want to quit or leave the conversation the only keyword output is the word quit. Use the previous_keywords list if a user asks a follow-up question to formulate a new question with keywords."},
            {"role": "user", "content": f"Extract the important keywords from the following query: {user_query}"},
        ]
    )
    keywords = response.choices[0].message.content
    return keywords

def query_ai(keywords, num_param, original_query):
    results = query(keywords, num_param)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an IT Search Engine Assistant. You are a part of the URI IT Service Desk (ITSD). Respond in a conversational manner. Your job is to go through the results of a query and find the most optimal answer to the proposed question, summarize it, and then return the shortened answer only. Only include information from the search results. Provide links for http websites on a new line when important to the question."},
        {"role": "user", "content": results},
        {"role": "user", "content": f"Here is the original query to find results for: {original_query}"},
    ]
    )
    return completion.choices[0].message.content