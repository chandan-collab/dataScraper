# dataScraper
This module can scrape information form any website and save them in QA format for AI training .

How it works:

1. Webpage will be scraped.

2. Its content will be cleaned and divided into chunks (as the entire page can be very large).

3. Generate a synthetic QA pair from each chunk:
    "question" = general question that can be asked about that chunk
    "answer" = text of that chunk (directly)

Example Output (qa_dataset.jsonl):
{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "question": "What is explained in this part? (section 1)", "answer": "Python is an interpreted, high-level, general-purpose programming language..."}
{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "question": "What is explained in this part? (section 2)", "answer": "Guido van Rossum created Python in 1989..."}


Now this format will be perfect for any of your English QA models (Hugging Face, OpenAI fine-tuning, LangChain retrievers, etc.).
