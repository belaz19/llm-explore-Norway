# Norway Tourist Guide
This is the "Norway Tourist Guide" app.It has a knowledge base of 150 most popular attractions in Norway of different kind: sightseeing, hiking, cruise, etc.
It provides you a user interface where you can ask a question related to tourist attractions in Norway and get an answer.
If you are planning your vacations in Norway, this is an app for you. You

## How to run the app on Linux
1. Open Terminal and run:
```
git clone https://github.com/belaz19/llm-explore-Norway.git
cd llm-explore-Norway/norway_guide
```

2. Get an OpenAI API key here `https://platform.openai.com/settings/organization/api-keys` and run in Terminal:
```
export OPENAI_API_KEY="insert_your_key_here"
```

3. Run docker:
```
docker compose build
docker compose up
```

4. Forward port 8501 (if not done automatically) and open it in broswer:
```
http://localhost:8501/
```

5. When stopped using the app, press `Ctrl + C` in Terminal and run this:
```
docker compose down
```

## How to use the app
Go to the User page, type your question into the box, click on "Get Answer", read the answer, provide a feedback if you like.
![User page](https://github.com/belaz19/llm-explore-Norway/blob/main/norway_guide/User_page.jpg)

## How to see performance metrics
Go to the Admin page, and see the metrics: Last 5 records, Feedback Distribution, Average Token Usage (Input & Output), Average Response Time, Queries in the Last Hour.
![Admin page](https://github.com/belaz19/llm-explore-Norway/blob/main/norway_guide/Admin_page.jpg)
