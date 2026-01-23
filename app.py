import streamlit
import chromadb
import requests


@streamlit.cache_resource
def init_chroma_db() -> chromadb.Collection:
    client = chromadb.PersistentClient(path="data/chromadb")
    return client.get_collection("media_reviews")


collection = init_chroma_db()


def generate_answer_with_ollama(query: str, retrieved_reviews: list[str]) -> str:
    context = "\n".join(retrieved_reviews)

    prompt = f"""
    Given the following reviews answer the question.
    If it's not enough data in reviews then just say it.

    Question: {query}

    Reviews: {context}
    """

    response = requests.post(
        url="http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


streamlit.title("🎬 ViewRAG: Analyzing Reviews about movies and tv shows")

streamlit.write("Ask me what you need!")

user_query = streamlit.text_input("Type your question:", placeholder="For example: 'What people thinks about 'Doctor Who'?")


if streamlit.button("Get answer"):
    if user_query:
        with streamlit.spinner("Searching relevant reviews and generating answer..."):
            results = collection.query(query_texts=[user_query], n_results=3)
            reviews = results['documents'][0]

            answer = generate_answer_with_ollama(user_query, reviews)

            streamlit.subheader("Answer:")
            streamlit.write(answer)

            with streamlit.expander("Show used reviews"):
                for i, review in enumerate(reviews):
                    streamlit.write(f"**Review {i + 1}:** {review[:200]}...")
    else:
        streamlit.warning("Please type your question")
