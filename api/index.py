"""Vercel function entrypoint for the GridGuide API.

Keeping the function under ``api/`` makes the route explicit for Vercel:
``/api/*`` is served by the FastAPI application in ``app.main``.
"""

from app.main import app

__all__ = ["app"]
