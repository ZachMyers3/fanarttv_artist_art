from dotenv import find_dotenv, load_dotenv
import json
import mutagen
import os
import pathlib
import requests

load_dotenv(find_dotenv())

FANARTTV_HOST = "https://webservice.fanart.tv"
FANARTTV_PORT = 443
FANARTTV_API_KEY = os.getenv("FANARTTV_API_KEY")
FANARTTV_ARTIST_PATH = f"{FANARTTV_HOST}/v3/music"

VALID_FILE_TYPES = [".mp3", ".flac", ".wav", ".mov", ".m4a"]


def get_first_file_in_directory(artist_path: pathlib.Path):
    for path in artist_path.iterdir():
        if path.is_dir():
            return get_first_file_in_directory(artist_path=path)
        else:
            if path.suffix.lower() in VALID_FILE_TYPES:
                return path


def get_arist_thumbnail_from_fanarttv(artist_id_combined: str):
    # request_uri = f"{FANARTTV_ARTIST_PATH}/{artist_id}"
    params = {}
    params["api_key"] = FANARTTV_API_KEY

    for artist_id in artist_id_combined.split("/"):
        request_uri = f"{FANARTTV_ARTIST_PATH}/{artist_id}"
        r = requests.get(request_uri, params=params)
        if r.ok:
            return r

    return None


def decode_string_if_needed(in_string: str) -> str:
    return_str = ""
    try:
        return_str = in_string.decode()
    except (UnicodeDecodeError, AttributeError):
        return_str = in_string

    return return_str


def get_artist_id(artist_path: pathlib.Path) -> str:
    music_file = get_first_file_in_directory(artist_path=artist_path)

    if music_file:
        music_file_metadata = mutagen.File(music_file)
        try:
            artist_id = music_file_metadata["TXXX:MusicBrainz Artist Id"]
            return decode_string_if_needed(artist_id.text[0])
        except KeyError:
            try:
                artist_id = music_file_metadata["musicbrainz_albumartistid"]
                return decode_string_if_needed(artist_id[0])
            except KeyError:
                try:
                    artist_id = music_file_metadata[
                        "----:com.apple.iTunes:MusicBrainz Album Artist Id"
                    ]
                    return decode_string_if_needed(artist_id[0])
                except KeyError:
                    # print(music_file_metadata)
                    print(f"Unable to find artist for {music_file.name}")
                    return ""
    else:
        return ""


def gather_art(path: pathlib.Path):
    artist_path_list = [x for x in path.iterdir() if x.is_dir()]

    params = {}
    params["api_key"] = FANARTTV_API_KEY

    for artist_path in artist_path_list:
        # assuming the folder name is the artist we're searching for
        artist_id = get_artist_id(artist_path=artist_path)
        # print(f"{artist_id=}")
        artist_info = get_arist_thumbnail_from_fanarttv(
            artist_id_combined=artist_id
        )
        if artist_info is None:
            continue

        artist_data = json.loads(artist_info.text)
        artist_thumbnails = None
        try:
            artist_thumbnails = artist_data["artistthumb"]
        except KeyError:
            continue

        print(f"=============== {artist_path.name} ===============")
        artist_thumnail_uri = artist_thumbnails[0]["url"]
        r = requests.get(artist_thumnail_uri, params=params, stream=True)
        artist_image_path = artist_path / "artist.jpg"
        with open(artist_image_path, "wb") as _w:
            for chunk in r.iter_content(1024):
                _w.write(chunk)
        # print(artist_thumnail_uri)


if __name__ == "__main__":
    gather_art()
