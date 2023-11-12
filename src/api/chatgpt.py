from openai import OpenAI
from os import getenv
import json


def make_yelp_query(prompt):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key= getenv("OPENAI_KEY"),
    )

    context = 'you are now a bot to translate human text to Yelp Business Search API parameters. You are going to help me construct a request by translating human text to parameters, but only return the json formatted text. You are going to return a json formatted response. Please return ONLY parameters the parameters "term", "categories" and "price" in the Business search API. If some parameters are not filled, fill it in as the string "null".'
    # prompt = "I want to find a nice chicken teriyaki place that's not too expensive and is also in santa clara county"

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",

    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt}
    ]
    )

    res = str(completion.choices[0].message)

    print(res + "\n")
    # a = "ChatCompletionMessage(content= {\n  \"term\": \"chicken teriyaki\",\n  \"categories\": \"null\",\n  \"price\": \"1,2\"\n}', role=\'assistant\', function_call=None, tool_calls=None)"
    # b = 'ChatCompletionMessage(content=\'{\n  "term": "chicken teriyaki",\n  "categories": "null",\n  "price": "$"\n}\', role=\'assistant\', function_call=None, tool_calls=None)'

    cleaned = ""
    read = 0
    for c in res:

        if c == "{":
            read = 1

        elif c == "}":
            read = 0
            
        if read == 1:
            cleaned += c

    cleaned += "}"
    print(cleaned)
    cleaned = cleaned.replace("\n", "")
    print(cleaned)
    # {\n  "term": "chicken teriyaki",\n  "categories": "null",\n  "price": "1,2"\n}
    yelp_query = json.loads(cleaned)

    for key, value in yelp_query.items():
        if value == "null":
            yelp_query[key] = None

    return yelp_query

prompt = "I want to find a nice chicken teriyaki place that's not too expensive and is also in santa clara county"
print(make_yelp_query(prompt))
