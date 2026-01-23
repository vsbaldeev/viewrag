import pandas
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.models.Collection import Collection

def load_reviews(item_type: str):
    reviews = pandas.read_csv(f"data/{item_type}s_reviews.csv")
    return reviews


def index_reviews(reviews: pandas.DataFrame, collection: Collection):
    ids = [str(i) for i in range(len(reviews))]

    documents = reviews["content"].tolist()

    metadatas = [
        {
            "review_id": row["review_id"],
            "created_at": row["created_at"],
        }
        for _, row in reviews.iterrows()
    ]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

def main():
    movies_reviews = load_reviews("movie")
    tvs_reviews = load_reviews("tv")
    all_reviews = pandas.concat([movies_reviews, tvs_reviews])

    client = chromadb.PersistentClient(path="data/chromadb")

    collection = client.get_or_create_collection(
        "media_reviews",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2"),
    )

    index_reviews(all_reviews, collection)


if __name__ == '__main__':
    main()
