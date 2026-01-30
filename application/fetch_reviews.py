import csv
import pandas
import requests
import secrets_manager


def get_item_reviews_dicts(api_key: str, item_type: str, item_id: str) -> list[dict]:
    print(f"getting reviews for {item_id}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }

    def get_results(item_type: str, item_id: str, page_counter: int, headers: dict) -> list[dict]:
        url = f"https://api.themoviedb.org/3/{item_type}/{item_id}/reviews"

        response = requests.get(url, headers=headers, params={"page": page_counter, "language": "en-US"})
        json = response.json()

        return [
            {
                "review_id": item.get("id"),
                "media_id": item_id,
                "created_at": item.get("created_at"),
                "content": item.get("content"),
            }
            for item in json["results"]
        ]


    page_counter = 1
    page_results = get_results(item_type, item_id, page_counter, headers)

    results = []

    while len(page_results) > 0:
        results += page_results
        page_counter += 1
        page_results = get_results(item_type, item_id, page_counter, headers)

    print("got " + str(len(results)) + " reviews")

    return results


def get_items_reviews(api_key: str, item_type: str, dataset: pandas.DataFrame) -> list[dict]:
    reviews = []

    for item_id in dataset["media_id"]:
        reviews += get_item_reviews_dicts(api_key, item_type, item_id)

    return reviews


def write_reviews_to_file(reviews: list[dict], filename: str) -> None:
    all_reviews_dataset = pandas.DataFrame(reviews)
    all_reviews_dataset.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)


def main():
    tmdb_api_key = secrets_manager.get("TMDB_API_KEY")

    movies_dataset = pandas.read_csv("../data/movies.csv")
    movies_reviews = get_items_reviews(tmdb_api_key, "movie", movies_dataset)
    write_reviews_to_file(movies_reviews, f"../data/movies_reviews.csv")

    movies_dataset = pandas.read_csv("../data/tvs.csv")
    tv_shows_reviews = get_items_reviews(tmdb_api_key, "tv", movies_dataset)
    write_reviews_to_file(tv_shows_reviews, f"../data/tvs_reviews.csv")


if __name__ == "__main__":
    main()
