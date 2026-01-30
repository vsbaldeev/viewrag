import streamlit
from llm_provider import LlmProvider
from search_engine import SearchEngine


llm_provider = LlmProvider()
search_engine = SearchEngine()


streamlit.title("🎬 ViewRAG: Analyzing Reviews about movies and tv shows")
streamlit.write("Ask me what you need!")

user_query = streamlit.text_input("Type your question:", placeholder="For example: 'What people thinks about 'Doctor Who'?")


def data_not_found():
    streamlit.warning("Please type your question")

if streamlit.button("Get answer"):
    if user_query:
        reviews = []

        with streamlit.spinner("Searching relevant reviews and generating answer..."):
            if not (media_title := llm_provider.extract_media_title(user_query)):
                streamlit.info("ℹ️ No specific media title detected. Performing semantic search across all reviews.")
                reviews = search_engine.search_with_query(user_query)
            else:
                reviews = search_engine.search_with_filters(user_query, media_title)

            if len(reviews) == 0:
                streamlit.info("ℹ️ No reviews found.")
                answer = "Try to use capitals or quoting media title."
            else:
                answer = llm_provider.generate_answer(user_query, reviews)
                streamlit.subheader("Answer:")
                streamlit.write(answer)

            with streamlit.expander("Show used reviews"):
                for i, review in enumerate(reviews):
                    streamlit.write(f"**Review {i + 1}:** {review[:200]}...")
    else:
        streamlit.warning("Please type your question")
