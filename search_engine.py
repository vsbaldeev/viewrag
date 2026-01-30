import pinecone
from pinecone.core.openapi.db_data.model.search_records_response import SearchRecordsResponse

import os

from dotenv import load_dotenv
load_dotenv(verbose=True)


class SearchEngine:
    def __init__(self):
        pinecone_client = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.__pinecone_dense_index = pinecone_client.Index(
            host=os.getenv("PINECONE_DENSE_INDEX_HOST"),
            pool_threads=10
        )
        self.__pinecone_sparse_index = pinecone_client.Index(
            host=os.getenv("PINECONE_SPARSE_INDEX_HOST"),
            pool_threads=10
        )

    def search_with_filters(self, query: str, media_title: str) -> list[str]:
        print(f"search_reviews for {media_title}")

        try:
            result: SearchRecordsResponse = self.__pinecone_dense_index.search(
                namespace="__default__",
                query={
                    "inputs": {"text": query},
                    "top_k": 3,
                    "filter": {"media_title": {"$eq": media_title.lower()}}
                },
                fields=["review"]
            )

            hits = result["result"]["hits"]
            return [hit["fields"]["review"] for hit in hits]
        except Exception as exception:
            print(exception)
            return []

    def search_with_query(self, query: str) -> list[str]:
        try:
            result: SearchRecordsResponse = self.__pinecone_dense_index.search(
                namespace="__default__",
                query={
                    "inputs": {"text": query},
                    "top_k": 3
                },
                fields=["media_title", "review"]
            )

            hits = result["result"]["hits"]
            return [
                f"Review about {hit['fields']['media_title']}: {hit['fields']['review']}"
                for hit in hits
            ]
        except Exception as exception:
            print(exception)
            return []
