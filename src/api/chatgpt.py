from openai import OpenAI
from os import getenv

from functools import cache

import json
import re


@cache
def make_yelp_query(input_prompt: str) -> tuple:
    client = OpenAI(
        api_key=getenv("OPENAI_KEY"),
    )

    context = 'you are now a bot to translate human text to Yelp Business Search API parameters. You are going to help me construct a request by translating human text to parameters, but only return the json formatted text. You are going to return a json formatted response. Please return ONLY parameters the parameters "term", "categories" and "price" in the Business search API. If some parameters are not filled, fill it in as the string "null".'
    # prompt = "I want to find a nice chicken teriyaki place that's not too expensive and is also in santa clara county"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",

        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": input_prompt}
        ]
    )

    res = str(completion.choices[0].message)

    print(res + "\n")

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
    cleaned = cleaned.replace("\\n", "")

    try:
        yelp_query = json.loads(cleaned)
    except json.JSONDecodeError:
        return None, None, None

    # for key, value in yelp_query.items():
    #     if value == "null":
    #         yelp_query[key] = None

    # Ensure that ChatGPT returns a comma-seperated list of integers and not dollar signs
    out_price = None
    if re.match("^[1-4]+(,\\s*[1-4]+)*$", yelp_query["price"]):
        out_price = yelp_query["price"]

    out_term = None
    if yelp_query.get("term", "null") != "null":
        out_term = yelp_query["term"]

    out_categories = None
    if yelp_query.get("categories", "null") != "null":
        out_categories = yelp_query["categories"]

    return out_term, out_categories, out_price


if __name__ == '__main__':
    prompt = "I want to find a nice chicken teriyaki place that's not too expensive and is also in santa clara county"
    print(make_yelp_query(prompt))
