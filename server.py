from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
import uvicorn
import threading
from fastmcp import FastMCP
import httpx
import os
from typing import Optional

mcp = FastMCP("PyMusixmatch")

BASE_URL = "https://api.musixmatch.com/ws/1.1"
API_KEY = os.environ.get("MUSIXMATCH_API_KEY", "")


def build_params(extra: dict) -> dict:
    """Build query params with API key, filtering out None values."""
    params = {"apikey": API_KEY, "format": "json"}
    for k, v in extra.items():
        if v is not None:
            params[k] = v
    return params


@mcp.tool()
async def get_chart_artists(
    page: int = 1,
    page_size: int = 10,
    country: Optional[str] = "US",
    format: Optional[str] = "json",
) -> dict:
    """Retrieve the top artists chart for a given country from Musixmatch.
    Use this when the user wants to discover popular or trending artists in a specific country."""
    params = build_params({
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "country": country.lower() if country else "us",
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/chart.artists.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def get_chart_tracks(
    page: int = 1,
    page_size: int = 10,
    f_has_lyrics: Optional[bool] = False,
    country: Optional[str] = "US",
    format: Optional[str] = "json",
) -> dict:
    """Retrieve the top tracks chart for a given country from Musixmatch.
    Use this when the user wants to discover trending or popular songs in a specific country,
    optionally filtered to only tracks that have lyrics."""
    params = build_params({
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "f_has_lyrics": 1 if f_has_lyrics else 0,
        "country": country.lower() if country else "us",
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/chart.tracks.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def search_tracks(
    q_track: Optional[str] = None,
    q_artist: Optional[str] = None,
    q_lyrics: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    f_has_lyrics: Optional[bool] = False,
) -> dict:
    """Search for tracks on Musixmatch by track title, artist name, or lyrics snippet.
    Use this when the user wants to find a specific song or look up tracks matching a query."""
    params = build_params({
        "q_track": q_track,
        "q_artist": q_artist,
        "q_lyrics": q_lyrics,
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "f_has_lyrics": 1 if f_has_lyrics else 0,
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/track.search", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_track_lyrics(
    track_id: int,
    format: Optional[str] = "json",
) -> dict:
    """Retrieve the full lyrics for a specific track by its Musixmatch track ID.
    Use this when the user wants to read or display the lyrics of a known track."""
    params = build_params({
        "track_id": track_id,
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/track.lyrics.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def get_track(
    track_id: int,
    format: Optional[str] = "json",
) -> dict:
    """Retrieve detailed metadata for a specific track by its Musixmatch track ID.
    Use this when the user wants information about a track such as title, artist, album, rating, or other attributes."""
    params = build_params({
        "track_id": track_id,
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/track.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def search_artists(
    q_artist: str,
    page: int = 1,
    page_size: int = 10,
    format: Optional[str] = "json",
) -> dict:
    """Search for artists on Musixmatch by name.
    Use this when the user wants to find an artist's Musixmatch profile, ID, or general information about them."""
    params = build_params({
        "q_artist": q_artist,
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/artist.search", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def get_artist_albums(
    artist_id: int,
    page: int = 1,
    page_size: int = 10,
    g_album_name: int = 1,
    s_release_date: Optional[str] = "desc",
    format: Optional[str] = "json",
) -> dict:
    """Retrieve the discography (list of albums) for a specific artist by their Musixmatch artist ID.
    Use this when the user wants to explore an artist's albums or find a particular album."""
    params = build_params({
        "artist_id": artist_id,
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "g_album_name": g_album_name,
        "s_release_date": s_release_date or "desc",
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/artist.albums.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()


@mcp.tool()
async def get_album_tracks(
    album_id: int,
    page: int = 1,
    page_size: int = 10,
    f_has_lyrics: Optional[bool] = False,
    format: Optional[str] = "json",
) -> dict:
    """Retrieve the list of tracks for a specific album by its Musixmatch album ID.
    Use this when the user wants to see the track listing of an album or find a specific song within it."""
    params = build_params({
        "album_id": album_id,
        "page": page,
        "page_size": max(1, min(100, page_size)),
        "f_has_lyrics": 1 if f_has_lyrics else 0,
        "format": format or "json",
    })
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/album.tracks.get", params=params)
        response.raise_for_status()
        if format == "xml":
            return {"xml": response.text}
        return response.json()




_SERVER_SLUG = "hudsonbrendon-python-musixmatch"

def _track(tool_name: str, ua: str = ""):
    try:
        import urllib.request, json as _json
        data = _json.dumps({"slug": _SERVER_SLUG, "event": "tool_call", "tool": tool_name, "user_agent": ua}).encode()
        req = urllib.request.Request("https://www.volspan.dev/api/analytics/event", data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=1)
    except Exception:
        pass

async def health(request):
    return JSONResponse({"status": "ok", "server": mcp.name})

async def tools(request):
    registered = await mcp.list_tools()
    tool_list = [{"name": t.name, "description": t.description or ""} for t in registered]
    return JSONResponse({"tools": tool_list, "count": len(tool_list)})

mcp_app = mcp.http_app(transport="streamable-http")

class _FixAcceptHeader:
    """Ensure Accept header includes both types FastMCP requires."""
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            accept = headers.get(b"accept", b"").decode()
            if "text/event-stream" not in accept:
                new_headers = [(k, v) for k, v in scope["headers"] if k != b"accept"]
                new_headers.append((b"accept", b"application/json, text/event-stream"))
                scope = dict(scope, headers=new_headers)
        await self.app(scope, receive, send)

app = _FixAcceptHeader(Starlette(
    routes=[
        Route("/health", health),
        Route("/tools", tools),
        Mount("/", mcp_app),
    ],
    lifespan=mcp_app.lifespan,
))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
