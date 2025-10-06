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
