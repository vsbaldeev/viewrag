from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing import Optional
import os
import langsmith

from dotenv import load_dotenv
load_dotenv(verbose=True)


__all__ = ["LlmProvider"]


class LlmProvider:
    def __init__(self) -> None:
        self.__extraction_title_model = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.0
        )
        self.__generation_model = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2
        )


    @langsmith.traceable
    def extract_media_title(self, query: str) -> Optional[str]:
        print("extract_media_title_with_llm")

        prompt = f"""
        Extract the movie or TV show title from this question. 
        Return ONLY the title, nothing else. If no title found, return "NONE".

        Question: {query}
        """
        print("Prompt: ", prompt)

        response = self.__extraction_title_model.invoke([HumanMessage(prompt)])
        content = response.content

        print("LLM Answer: ", content)

        result = content.strip()
        return result if result != "NONE" else None

    @langsmith.traceable
    def generate_answer(self, query: str, retrieved_reviews: list[str]) -> str:
        print("generate_answer_with_groq")

        context = "\n".join(retrieved_reviews)

        prompt = f"""
        Given the following reviews answer the question.
        If it's not enough data in reviews then just say it.

        Question: {query}

        Reviews: {context}
        """

        print("Prompt: ", prompt)

        try:
            response = self.__extraction_title_model.invoke([HumanMessage(prompt)])

            return response.content

        except Exception as exception:
            return (
                "Sorry, I can't help you. Please try again."
                f"Error: {exception}"
            )
