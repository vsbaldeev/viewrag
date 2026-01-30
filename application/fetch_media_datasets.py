import requests
import streamlit
import pandas
import csv
import secrets_manager

def get_top_movies_json(api_key: str, start_date: str, end_date: str) -> dict:
    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "sort_by": "popularity.desc",
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "page": 1
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    json_result =  response.json()

    print(f"total results = {json_result["total_results"]}")
    print(f"total pages = {json_result["total_pages"]}")

    return json_result


def get_top_tv_shows_json(api_key: str, start_date: str, end_date: str) -> dict:
    url = "https://api.themoviedb.org/3/discover/tv"

    params = {
        "sort_by": "popularity.desc",
        "first_air_date.gte": start_date,
        "first_air_date.lte": end_date,
        "page": 1
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    json_result = response.json()

    print(f"total results = {json_result["total_results"]}")
    print(f"total pages = {json_result["total_pages"]}")

    return json_result


def write_to_csv(json_dict, filename: str) -> None:
    ids = [item["id"] for item in json_dict["results"]]
    titles = [item.get("title") or item.get("name") for item in json_dict["results"]]
    release_dates = [item.get("release_date") or item.get("first_air_date") for item in json_dict["results"]]

    data_frame = pandas.DataFrame({
        "media_id": ids,
        "media_title": titles,
        "release_date": release_dates
    })

    data_frame.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)


def main():
    tmdb_api_key = secrets_manager.get("TMDB_API_KEY")
    start_date = "2015-12-31"
    end_date = "2025-12-31"

    movies_dict = get_top_movies_json(tmdb_api_key, start_date, end_date)
    write_to_csv(movies_dict, f"../data/movies.csv")

    tv_shows_dict = get_top_tv_shows_json(tmdb_api_key, start_date, end_date)
    write_to_csv(tv_shows_dict, f"../data/tvs.csv")
    write_to_csv(movies_dict, f"data/movies.csv")

    tv_shows_dict = get_top_tv_shows_json(tmdb_api_key, start_date, end_date)
    write_to_csv(tv_shows_dict, f"data/tvs.csv")


if __name__ == '__main__':
    main()
