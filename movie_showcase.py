import concurrent.futures
import os
from imdb import Cinemagoer
from re import sub

from pymongo import MongoClient


mongo_client = MongoClient()
movie_collection = mongo_client.get_database("movie_showcase").get_collection("movies")
actor_collection = mongo_client.get_database("movie_showcase").get_collection("actors")
movies_in_db = [
    item["torrent_file"]
    for item in list(movie_collection.find(projection={"_id": 0, "torrent_file": 1}))
]
movieids_in_db = [
    item["_id"] for item in list(movie_collection.find(projection={"_id": 1}))
]

actors_in_db = [
    item["_id"] for item in list(actor_collection.find(projection={"_id": True}))
]


def get_movie_info(movieTitle):
    try:
        print(f"Getting info for {movieTitle}")
        cg = Cinemagoer()
        mov = cg.search_movie(title=movieTitle)
        if mov:
            mov = mov[0]
        else:
            return None

        if mov.movieID in movieids_in_db:
            return None
        movie_data = cg.get_movie(
            mov.movieID, info=["main", "plot", "quotes", "synopsis", "release dates"]
        )

        cast = (
            [actor.personID for actor in movie_data.get("cast")]
            if movie_data.get("cast")
            else []
        )
        cast.extend([d.personID for d in movie_data.get("director") or []])
        cast.extend([p.personID for p in movie_data.get("producer") or []])
        new_actors = [actor for actor in cast if actor not in actors_in_db]

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            cg = Cinemagoer()
            actor_infos = []
            for actor in new_actors:
                cg = Cinemagoer()
                try:
                    actor_infos.append(executor.submit(cg.get_person, actor))
                except:
                    print("Error")
            for actor_info in concurrent.futures.as_completed(actor_infos):
                try:
                    actor_data = actor_info.result()
                    if actor_data:
                        actor = {
                            "_id": actor_data.personID,
                            "name": actor_data.get("name"),
                            "full size photo": actor_data.get("full-size headshot"),
                            "photo": actor_data.get("headshot"),
                        }

                        try:
                            actor_collection.insert_one(actor)
                            actors_in_db.append(actor["_id"])
                        except Exception:
                            continue
                        print(f"Actor added: {actor_data['name']}")
                except Exception:
                    print("exception")

        movie = {
            "_id": movie_data.movieID,
            "title": movie_data.get("title").strip(' "'),
            "torrent_file": movieTitle,
            "plot": movie_data.get("plot"),
            "rating": movie_data.get("rating"),
            "genres": movie_data.get("genres"),
            "original air date": movie_data.get("original air date"),
            "director": [d.personID for d in movie_data.get("director") or []],
            "producer": [p.personID for p in movie_data.get("producer") or []],
            "synopsis": movie_data.get("synopsis"),
            "poster": movie_data.get("full-size cover url"),
            "cast": {
                actor.personID: {"name": actor["name"], "role": str(actor.currentRole)}
                for actor in (movie_data.get("cast") or [])
            },
        }
        return movie
    except Exception as e:
        print(f"Exception while getting movie data for {movieTitle}")
        print(e)
        return None


def get_movie_names_from_torrents(files):
    junk_words = [
        ".torrent",
        "DTS",
        "15.1",
        "AC3",
        "4K",
        "2160*",
        "rarbg",
        "S0.*",
        "rartv",
        "\[.*\]",
        "COMPLETE",
        "NF",
        "DDP5",
        "1080p",
        "WEBRip",
        "6CH",
        "10bit",
        "BluRay",
        "HEVC",
        "WEB-DL",
        "x265",
        "x264",
        "HEVC-PSA",
    ]
    torrent_files = [
        sub(
            "|".join(junk_words),
            "",
            sub(r"(\(\d{4}\)).*", r"\1", sub(r"www\..*?\s", "", file)),
        ).strip("- .")
        for file in files
        if file.endswith(".torrent")
    ]
    return set(torrent_files)


def last_modified(file):
    return os.path.getmtime(file)


if __name__ == "__main__":
    directory = "/Users/gijomathew/Torrents/torrent files"
    filenames = os.listdir(directory)
    sorted_filenames = sorted(
        filenames, key=lambda x: last_modified(os.path.join(directory, x))
    )

    movs = get_movie_names_from_torrents(sorted_filenames)
    new_movies = [mov for mov in movs if mov not in movies_in_db]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        movie_infos = [executor.submit(get_movie_info, mov) for mov in new_movies]
        for movie_info in concurrent.futures.as_completed(movie_infos):
            try:
                mov_result = movie_info.result()
                if mov_result:
                    movie_collection.insert_one(mov_result)
                    print(f"Movie added: {mov_result['title']}")
                    print("\n")
            except Exception as e:
                print(f"exception occurred for {movie_info}")
                print(e)
                break
