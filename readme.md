# Personal Web Memory - End-to-End Demo

A lightweight system that turns your browsing history into a searchable personal memory layer.  
This project demonstrates the full workflow Sid requested: capture -> process -> index -> retrieve -> agent -> UI.

Built using Python, BeautifulSoup, Chroma, LangChain, OpenAI Embeddings, and Streamlit.

--------

## What This Project Does

This system takes raw browsing behavior (Chrome history), processes it, builds a vector index, and exposes an intelligent agent that can answer questions such as:
- "What product pages did I look at?"
- "Which pages did I visit about AirPods?"
- "Show me the page I looked at about agents this week."

It includes:
1. History extraction  
2. Web page scraping + fallback logic  
3. Embedding + vector store indexing  
4. A retrieval-grounded QA agent with a custom prompt  
5. A simple Streamlit UI for running queries  

Everything runs locally and persists to `./data/chroma_db`.

------

## Project Architecture

Chrome History  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
`scrape_pages.py` — extract + clean content (title fallback)  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
`build_index.py` — embed & store in Chroma  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
`agent.py` — RetrievalQA agent over vector store  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
`streamlit_app.py` — simple UI for querying  

-----

### Repository Structure

```text
personal-web-memory/
│
├── extract_history.py
├── scrape_pages.py
├── build_index.py
├── agent.py
├── streamlit_app.py
│
├── requirements.txt
├── README.md
│
└── data/
    ├── scraped_pages.jsonl
    ├── profile.json           (optional)
    └── chroma_db/             (auto-created)


### Setup Instructions
	1.	Create virtual environment

python3 -m venv .venv
source .venv/bin/activate

	2.	Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

	3.	Add your OpenAI API key

Create .env or export manually:

export OPENAI_API_KEY=your_key_here


⸻

Extract Your Chrome History

python extract_history.py

Produces:

data/chrome_history.csv


⸻

Scrape Visited Pages

python scrape_pages.py

Produces:

data/scraped_pages.jsonl

Includes fallback logic: if pages block scraping and return empty content, the system uses the page title + URL so every page still contributes meaningfully to the memory.

⸻

Build the Vector Index

python build_index.py

This:
	•	Embeds each page using OpenAI’s text-embedding-3-small
	•	Stores them inside a persistent Chroma DB
	•	Prints how many documents were indexed (useful sanity check)

Generates:

data/chroma_db/


⸻

Run the Personal Web Memory Agent

python agent.py

This loads the index and answers a sample query.
The agent uses a custom retrieval-grounded prompt:
	•	It must answer only using retrieved context
	•	If nothing is relevant, it returns:
"I couldn’t find that in your browsing history."

⸻

Run the Streamlit App

streamlit run streamlit_app.py

Open your browser at:

http://localhost:8501

You will see a single input box.
Ask questions like:

✅ Example queries
	•	“What product pages did I visit recently?”
	•	“Show me the pages I viewed about AirPods.”
	•	“What pages did I read about watches?”
	•	“Which shopping sites did I open this week?”
	•	“Summarize the product pages I looked at.”

⸻

Agent Prompting Logic

The RetrievalQA agent is intentionally simple:
	•	Query → embed → retrieve top-k documents
	•	Agent answers using only retrieved text
	•	Encourages grounding, reduces hallucination
	•	Fallback line when there is truly no match

This models the early version of what Nora’s personal-shopping memory layer would do.

⸻

Debugging Tools Included
	•	build_index.py prints how many documents were added
	•	agent.py (optional mode) prints source documents used
	•	Scraper includes error handling for blocked websites
	•	Index rebuild wipes old DB to avoid stale embeddings

