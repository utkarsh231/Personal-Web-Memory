from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
#from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# fixing Streamlit issue
try:
    from langchain.chains import RetrievalQA
except ImportError:  
    from langchain.chains.retrieval_qa.base import RetrievalQA

def load_agent():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma(
        collection_name="personal_web_memory",
        embedding_function=embeddings,
        persist_directory="./data/chroma_db",
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt_template = """
You are a personal web memory assistant.

You are given CONTEXT that was scraped from the user's own browsing history
(web pages they visited, including product pages, articles, and tools).

- If the context contains any pages that are even partially relevant,
  list the most relevant ones and describe them briefly.
- Only say "I couldn't find that in your browsing history." if the context
  is completely unrelated or empty.


CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    return qa


agent = load_agent()


def ask(query: str) -> str:
    result = agent.invoke({"query": query})
    answer = result["result"]
    return answer


if __name__ == "__main__":
    print(ask("What product did I look at?"))