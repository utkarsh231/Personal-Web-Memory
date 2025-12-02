import json
from openai import OpenAI

client = OpenAI()

def generate_profile():
    docs = []

    with open("./data/scraped_pages.jsonl", "r") as f:
        for line in f: 
            docs.append(json.loads(line))

        
    titles = [d["title"] for d in docs if d.get("title")]
    title_preview = "\n".join(titles[:50])

    prompt = f"""
    You are analyzing a user's recent web browsing history.
    Here are some of the page titles they visited recently:
    {title_preview}

    Based on these titles, infer 5-7 personal interests, shopping preferences, or habits.
    Focus on things like categories they care about (e.g. tech gadgets, shoes, fitness),
    sites they tend to use, and any obvious themes.set

    Return your answer as a short markdown list, no extra commentary.
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": prompt}
        ],
    )

    profile = resp.choices[0].message.content

    with open("./data/profile.json", "w") as f:
        json.dump({"profile": profile}, f, indent=2)

    print("Profile generated and saved to ./data/profile.json")
    print(profile)

if __name__ == "__main__":
    generate_profile()