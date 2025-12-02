from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import json, os, shutil

DATA_DIR = "./data"
SCRAPED_PATH = os.path.join(DATA_DIR, "scraped_pages.jsonl")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
COLLECTION_NAME = "personal_web_memory"


def build_index():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(SCRAPED_PATH):
        raise FileNotFoundError(f"Missing {SCRAPED_PATH} – did you run scrape_pages.py?")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Start fresh while debugging
    if os.path.exists(CHROMA_DIR):
        print("Removing existing Chroma DB...")
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    added = 0
    with open(SCRAPED_PATH, "r") as f:
        for line in f:
            doc = json.loads(line)

            # 1) Try page content
            content = doc.get("content") or ""

            # 2) Fallback to title + URL if content is empty
            if not content.strip():
                title = doc.get("title") or ""
                url = doc.get("url") or ""
                content = f"{title}\n{url}"

            # Still skip totally empty / junk lines
            if len(content.strip()) < 10:
                continue

            vectorstore.add_texts(
                texts=[content],
                metadatas=[{
                    "url": doc.get("url"),
                    "title": doc.get("title"),
                    "timestamp": doc.get("timestamp"),
                }],
                ids=[doc.get("url") or str(added)],
            )
            added += 1

    # Not strictly needed in newer Chroma, but harmless
    vectorstore.persist()
    print(f"Index built and persisted. Added {added} documents.")


if __name__ == "__main__":
    build_index()