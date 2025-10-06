# Norway Tourist Guide

## Problem description
When you are going on vacations to Norway (or any other country), you should get familiar with what this country has to offer. What are the most popular tourist attractions, where are they located, what is the best time of year to visit them. The goal of this project is to:
1. Create a knowledge base of most popular attractions in Norway
2. Create a RAG (Retrieval-Augmented Generation) flow  which recieves a question from a user and generates an answer with LLM; evaluate different Retrieval and LLM models to fine-tune this RAG flow
3. Create an application with an User Interface, where users can ask questions about tourist attractions in Norway and get answers that help them planning vacations and not missing out important tourist attractions

## Retrieval flow
All my scipts used for discovering the best RAG flow and its components are stored in the folder `notebooks`.
My RAG flow is created in the `make_rag.ipynb` notebook:
```
def rag(query):
    search_results = search(query) # a search function that search over the Knowledge base and choose the most relevant records based on the user's query
    prompt = build_prompt(query, search_results) # a prompt build function that builds an LLM-suitable prompt based on the users's query and search results
    answer = llm(prompt) # a function sending the prompt to llm and receiving an answer from llm
    return answer # the RAG flow returns that LLM answer to the user
```

## Retrieval evaluation
First the `ground-truth-data.csv` is generated using the `make_truth.ipynb` notebook. This .csv document contains 5 questions to each record in the knowledge base. The retrieval evaluation is done using the 'eval_retrieval.ipynb' notebook.

Multiple retrieval approaches are evaluated, and the best one is used.
The evaluated retrieval approahces:
1. minsearch without boosting: hit rate 98%, mrr 94%
2. minsearch with boosting: hit rate 99%, mrr 97%

Thus, minsearch with boosting is selected going forward:
```
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
```

## LLM evaluation
The notebook `eval_llm.ipynb` is used to evaluate LLMs. Multiple approaches are evaluated, and the best one is used.
100 random questions are chosen from `ground-truth-data.csv`, then answered by LLMs and then evaluated by LLM whether they are relevant or not.

The evaluated LLMs:
1. answered by gpt-5-mini (and then evaluated by gpt-5-mini): RELEVANT 83, PARTLY_RELEVANT 15, NON_RELEVANT 2
2. answered by gpt-5-nano (and then evaluated by gpt-5-mini): RELEVANT 82, PARTLY_RELEVANT 15, NON_RELEVANT 3

Thus, the LLM model gpt-5-mini is selected going forward:
```
def llm(prompt, model = 'gpt_5-mini'):
    response = client.chat.completions.create(
        model = model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
```

## Interface
Streamlit application is created for users to submit their questions about tourist attractions in Norway, get answers and submit feedback.

All details about the app can be found in the folder 'norway_guide'. The app is scripted in the file `app.py`.

## Ingestion pipeline
There is an automated ingestion of the dataset `data.csv` into the knowledge base, it's done by the Python script `rag.py` when users starts the Streamlit app.

## Monitoring
The user feedback is collected and there's a dashboard with 5 charts.
When a user starts the application `monitor.db` database and `monitor` table are initiated using SQLite. This table is used to store information such as: timestamp, query, prompt, answer, feedback, response_time, input_tokens, output_tokens.
The Streamlit app has an Admin page, where an admin can see the performance / feedback metrics from that `monitor` tabel.

All details about the app can be found in the folder 'norway_guide'. The app is scripted in the file `app.py`.
