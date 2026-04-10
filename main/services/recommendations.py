from .tmdb import tmdb_request
from .mal import mal_request       
from .dex import dex_request       



def get_tmdb_recommendations(external_id, media_type):
    """
    TMDB has a native /recommendations endpoint — use it directly.
    Returns a list of dicts shaped like your other detail results.
    """
    data = tmdb_request(f"{media_type}/{external_id}/recommendations")
    results = data.get("results", [])

    recs = []
    for item in results[:10]:
        recs.append({
            "title":       item.get("title") or item.get("name"),
            "external_id": str(item["id"]),
            "media_type":  media_type,
            "source":      "tmdb",
            "poster":      f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                           if item.get("poster_path") else "",
            "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
            "score":       item.get("vote_average"),
        })
    return recs



def get_mal_recommendations(external_id):
    """
    MAL's recommendations endpoint returns what other users paired this with.
    """
    data = mal_request(
        f"anime/{external_id}/recommendations",
        params={"limit": 10}
    )
    entries = data.get("data", [])

    recs = []
    for entry in entries:
        node = entry.get("node", {})
        recs.append({
            "title":       node.get("title"),
            "external_id": str(node["id"]),
            "media_type":  "anime",
            "source":      "mal",
            "poster":      node.get("main_picture", {}).get("medium", ""),
            "release_year": None,
            "score":       None,
        })
    return recs



def get_mangadex_recommendations(external_id):
    """
    MangaDex has no native recommendations endpoint.
    Strategy: fetch the manga's genres/tags, then search for
    other manga sharing those tags, excluding the original.
    """
    manga_data = dex_request(f"manga/{external_id}", params={"includes[]": "tag"})
    attributes = manga_data.get("data", {}).get("attributes", {})
    tags = attributes.get("tags", [])

    tag_ids = [t["id"] for t in tags[:3]]   

    if not tag_ids:
        return []

    
    params = {
        "includedTags[]": tag_ids,
        "excludedManga[]": [external_id],
        "limit": 10,
        "order[followedCount]": "desc",     
        "includes[]": ["cover_art"],
    }
    search_data = dex_request("manga", params=params)
    results = search_data.get("data", [])

    recs = []
    for item in results:
        attr = item.get("attributes", {})

        
        cover_rel = next(
            (r for r in item.get("relationships", []) if r["type"] == "cover_art"),
            None
        )
        cover_url = ""
        if cover_rel:
            filename = cover_rel.get("attributes", {}).get("fileName", "")
            cover_url = f"https://uploads.mangadex.org/covers/{item['id']}/{filename}.256.jpg"

        title_obj = attr.get("title", {})
        title = title_obj.get("en") or next(iter(title_obj.values()), "Unknown")

        recs.append({
            "title":       title,
            "external_id": item["id"],
            "media_type":  "manga",
            "source":      "mangadex",
            "poster":      cover_url,
            "release_year": attr.get("year"),
            "score":       None,
        })
    return recs



def get_recommendations_for_media(source, external_id, media_type):
    """
    Route to the correct recommendation function by source.
    Returns a list of recommendation dicts, or [] on failure.
    """
    try:
        if source == "tmdb":
            return get_tmdb_recommendations(external_id, media_type)
        elif source == "mal":
            return get_mal_recommendations(external_id)
        elif source == "mangadex":
            return get_mangadex_recommendations(external_id)
    except Exception:
        return []
    return []