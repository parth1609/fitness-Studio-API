"""Main application entrypoint for the Fitness Studio Booking API.

Exposes a minimal FastAPI app with a healthcheck endpoint. Routers for
authentication, classes, and bookings will be registered here as they are
implemented.

All documentation follows the project's Code Documentation Rulebook.
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI
from app.routers import auth, classes

app = FastAPI(
    title="Fitness Studio Booking API",
    version="0.1.0",
    description=(
        "API for user signup/login, managing fitness classes, and booking slots. "
        "Backed by SQLite and implemented with FastAPI."
    ),
)


@app.get("/health", tags=["health"])  # response intentionally simple
def health() -> dict:
    """Simple healthcheck endpoint.

    Returns a small JSON payload with current UTC time to ease basic monitoring.

    Returns
    -------
    dict
        An object with keys: ``status`` and ``time``.
    """
    return {"status": "ok", "time": datetime.now(tz=timezone.utc).isoformat()}


# Routers
app.include_router(auth.router)
app.include_router(classes.router)

