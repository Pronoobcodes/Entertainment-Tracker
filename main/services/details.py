from .tmdb import get_tmdb_details, tmdb_request
from .mal import get_mal_details
from .dex import get_manga_details


def detect_tmdb_type(external_id):
    data = tmdb_request(f"/search/multi", {"query": external_id})

    for item in data.get("results", []):
        if str(item.get("id")) == str(external_id):
            return item.get("media_type")

    return None


def get_details(source, external_id, media_type=None):
    if source == "tmdb":
        if not media_type:
            media_type = detect_tmdb_type(external_id)

        if not media_type:
            raise ValueError("Unable to determine TMDB media type")

        return get_tmdb_details(external_id, media_type)

    if source == "mal":
        return get_mal_details(external_id)

    if source == "mangadex":
        return get_manga_details(external_id)

    raise ValueError("Invalid content source")
