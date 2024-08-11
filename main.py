from inverted_index import query
from openai_parameters import extract_keywords
from openai_parameters import query_ai

user_query = ""

print("---------------------------------------------------------")
user_query = input("Enter query: ")
print()
keywords = extract_keywords(user_query)

while keywords != "quit":
    results_param = 10
    print(query_ai(keywords, results_param, user_query))

    print("---------------------------------------------------------")

    user_query = input("Enter query: ")
    print()
    keywords = extract_keywords(user_query)




