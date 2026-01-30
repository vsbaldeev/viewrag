import pandas
import pinecone
import os
import itertools
import uuid
import streamlit

def load_reviews(item_type: str) -> pandas.DataFrame:
    reviews = pandas.read_csv(f"data/{item_type}s_reviews.csv")
    return reviews


def load_media_df(item_type: str) -> pandas.DataFrame:
    df = pandas.read_csv(f"data/{item_type}s.csv")
    return df


def create_records_for_pinecone(reviews: pandas.DataFrame, media_df: pandas.DataFrame) -> list[dict]:
    print("Creating records for Pinecone")

    reviews_with_title = reviews.merge(media_df[["media_id", "media_title"]], how="inner", on="media_id")

    return [
        {
            "_id": str(uuid.uuid4()),
            "review": row["content"],
            "media_title": row["media_title"].lower(),
            "created_at": row["created_at"]
        }
        for _, row in reviews_with_title.iterrows()
    ]


def chunks(iterable, batch_size):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def main():
    movies_reviews = load_reviews("movie")
    tvs_reviews = load_reviews("tv")
    all_reviews = pandas.concat([movies_reviews, tvs_reviews])

    movie_df = load_media_df("movie")
    tv_df = load_media_df("tv")
    all_media_df = pandas.concat([movie_df, tv_df])

    pinecone_client = pinecone.Pinecone(api_key=streamlit.secrets.get("PINECONE_API_KEY"))
    pinecone_dense_index = pinecone_client.Index(host=streamlit.secrets.get("PINECONE_DENSE_INDEX_HOST"), pool_threads=10)
    pinecone_sparse_index = pinecone_client.Index(host=streamlit.secrets.get("PINECONE_SPARSE_INDEX_HOST"), pool_threads=10)
    records = create_records_for_pinecone(all_reviews, all_media_df)
    namespace = "__default__"

    for chunk in chunks(records, batch_size=96):
        pinecone_dense_index.upsert_records(namespace=namespace, records=chunk)
        pinecone_sparse_index.upsert_records(namespace=namespace, records=chunk)


if __name__ == '__main__':
    main()
