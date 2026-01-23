from main.services.tmdb import get_tmdb_details
from main.services.mal import get_mal_details
from main.services.dex import get_manga_details


def get_details(source, external_id, media_type=None):
    if source == "tmdb":
        if not media_type:
            raise ValueError("media_type required for TMDB")
        return get_tmdb_details(external_id, media_type)

    if source == "mal":
        return get_mal_details(external_id)

    if source == "mangadex":
        return get_manga_details(external_id)

    raise ValueError("Unknown source")
