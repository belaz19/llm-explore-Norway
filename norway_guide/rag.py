import pandas as pd
import os
from openai import OpenAI
import minsearch

# --- Load data and initialize index ---
df = pd.read_csv("data.csv")
documents = df.to_dict(orient="records")

index = minsearch.Index(
    text_fields=['attraction', 'activity_type', 'county', 'time_to_visit', 'description'],
    keyword_fields=['id']
)
index.fit(documents)

# --- OpenAI client setup ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your environment.")
client = OpenAI(api_key=api_key)

# --- Templates ---
prompt_template = """
You're a tourist guide in Norway. Answer the QUESTION based on the CONTEXT from our attractions database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

entry_template = """
attraction: {attraction}
activity_type: {activity_type}
county: {county}
time_to_visit: {time_to_visit}
description: {description}
""".strip()

# --- Helper functions ---
def search(query):
    boost = {
        'attraction': 3,
        'activity_type': 2,
        'county': 2,
        'time_to_visit': 1,
        'description': 1
    }

    results = index.search(
        query=query,
        filter_dict={},
        boost_dict=boost,
        num_results=5
    )
    return results

def build_prompt(query, search_results):
    context = ""
    for doc in search_results:
        context += entry_template.format(**doc) + "\n\n"
    return prompt_template.format(question=query, context=context).strip()

def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-5-mini',
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    return answer, input_tokens, output_tokens

def rag(query):
    # Perform search
    search_results = search(query)

    # Build prompt
    prompt = build_prompt(query, search_results)

    # Call LLM
    answer, input_tokens, output_tokens = llm(prompt)

    # Return all metrics, including the prompt
    return answer, input_tokens, output_tokens, prompt