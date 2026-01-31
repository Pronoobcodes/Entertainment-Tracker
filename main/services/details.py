from .tmdb import get_tmdb_details
from .mal import get_mal_details
from .dex import get_manga_details


def get_details(source, external_id, media_type=None):
    if source == "tmdb":
        return get_tmdb_details(external_id, media_type)

    if source == "mal":
        return get_mal_details(external_id)

    if source == "mangadex":
        return get_manga_details(external_id)

    raise ValueError("Invalid content source")
