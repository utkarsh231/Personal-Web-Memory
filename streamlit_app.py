"""
Build a small “personal web memory” system that shows you can scrape pages, process documents, and use an LLM (via LangChain) 
to retrieve useful information.

Your task is to pull your own Chrome history (URLs + titles + timestamps), visit those pages, scrape the main text content, 
and store everything in a simple local document index. You can use any stack you want for scraping and any vector store you prefer.

Once the pages are indexed, generate a tiny “profile” from the data using an LLM — just a few inferred preferences or 
interests based on the kinds of pages you visited. 
Then, using LangChain, create a minimal agent that can answer questions grounded in your scraped history, 
such as “What shoe did I look at?” or “Show me that article about agents I opened this week.”

Lastly, include a tiny UI (even a single input box is fine) where you can ask questions and get back an answer 
with relevant links or snippets. Keep everything lightweight. A short README explaining how to run it is enough.

The goal is simply to demonstrate end-to-end ability in scraping, document processing, retrieval, and basic agent design.

THE PLAN:

Chrome History -> Scraper -> Cleaner -> Embeddings            ->         Vector Store
                             |-> LLM Profile Generator    <- |- Agent     
                                |-> Streamlit UI
"""     


import streamlit as st
from agent import ask

st.title("Personal Web Memory Agent")
query = st.text_input("Ask a question about your web history:")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        answer = ask(query)
    st.write(answer)
