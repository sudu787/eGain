"""GridGuide demonstration API.

This service stores fictional outage reports for demonstration only. It is not
connected to an electric utility and does not dispatch crews or confirm outages.
"""

from __future__ import annotations

import hmac
import os
import re
import sqlite3
import uuid
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import psycopg
from fastapi import FastAPI, Header, HTTPException, Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from psycopg.rows import dict_row


APP_TITLE = "GridGuide Demonstration API"
DATABASE_URL = (
    os.getenv("GRIDGUIDE_DATABASE_URL")
    or os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
    or os.getenv("NEON_DATABASE_URL")
)
DB_PATH = Path(os.getenv("GRIDGUIDE_DB_PATH", "./data/gridguide.sqlite3"))
SQL_PARAM = "%s" if DATABASE_URL else "?"
DB_ERRORS = (psycopg.Error, OSError) if DATABASE_URL else (sqlite3.Error, OSError)
API_KEY = os.getenv("GRIDGUIDE_API_KEY", "")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("GRIDGUIDE_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
SERVICE_AREAS = {"North Ridge", "Cedar Park", "Riverbend", "Old Town"}
ISSUE_TYPES = {"no_power", "partial_power", "flickering_lights", "other"}
IDEMPOTENCY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")

DEMO_OUTAGES = [
    {
        "area": "North Ridge",
        "condition": "sample outage",
        "affected_blocks": 3,
        "status": "crew assigned (sample data)",
    },
    {
        "area": "Riverbend",
        "condition": "sample partial outage",
        "affected_blocks": 1,
        "status": "assessment pending (sample data)",
    },
]


class OutageReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_area: str = Field(min_length=1, max_length=40)
    issue_type: str = Field(min_length=1, max_length=32)


class OutageReportReceipt(BaseModel):
    reference: str
    service_area: str
    issue_type: str
    created_at: str
    status: str = "received for demonstration only"
    demo_notice: str = (
        "This report is stored in a fictional demo system. It was not sent to a utility."
    )


def connect_db() -> sqlite3.Connection | psycopg.Connection:
    if DATABASE_URL:
        return psycopg.connect(DATABASE_URL, row_factory=dict_row)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 10000")
    return connection


@contextmanager
def db_connection():
    connection = connect_db()
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize_db() -> None:
    # Vercel functions have ephemeral filesystems. Do not silently create a
    # SQLite database there; require the configured managed Postgres store.
    if os.getenv("VERCEL") and not DATABASE_URL:
        return
    with db_connection() as connection:
        if not DATABASE_URL:
            connection.execute("PRAGMA journal_mode = WAL")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS outage_reports (
                reference TEXT PRIMARY KEY,
                service_area TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                idempotency_key TEXT UNIQUE
            )
            """
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_db()
    yield


app = FastAPI(
    title=APP_TITLE,
    description=(
        "Synthetic outage-report actions and clearly labeled sample status data. "
        "No live utility system is connected."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
    )


@app.get("/healthz", tags=["service"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": "demonstration",
        "report_store": "configured" if DATABASE_URL or not os.getenv("VERCEL") else "not configured",
    }


@app.get("/api/v1/demo/outages", tags=["demonstration data"])
def list_demo_outages() -> dict[str, object]:
    return {
        "data_type": "synthetic demonstration data; not live utility status",
        "outages": DEMO_OUTAGES,
    }


def require_api_key(authorization: str | None) -> None:
    """Protect write/read actions when a deployment configures a shared secret."""
    if not API_KEY:
        return
    expected = f"Bearer {API_KEY}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Valid API credentials are required."},
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_report_storage() -> None:
    if os.getenv("VERCEL") and not DATABASE_URL:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "report_store_not_configured",
                "message": "The demonstration report store is not configured yet. No report was saved.",
            },
        )


@app.post(
    "/api/v1/outage-reports",
    response_model=OutageReportReceipt,
    status_code=201,
    tags=["demonstration actions"],
    summary="Create a fictional outage report",
)
def create_outage_report(
    request: OutageReportRequest,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    authorization: Annotated[str | None, Header()] = None,
) -> OutageReportReceipt:
    require_api_key(authorization)
    require_report_storage()
    area = request.service_area.strip()
    issue_type = request.issue_type.strip()
    if area not in SERVICE_AREAS:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "unknown_service_area",
                "message": "Choose one of the fictional demonstration service areas.",
                "allowed_values": sorted(SERVICE_AREAS),
            },
        )
    if issue_type not in ISSUE_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "unknown_issue_type",
                "message": "Choose a supported outage category.",
                "allowed_values": sorted(ISSUE_TYPES),
            },
        )
    if idempotency_key is not None and not IDEMPOTENCY_PATTERN.fullmatch(
        idempotency_key
    ):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_idempotency_key",
                "message": "Idempotency-Key must be 8–128 letters, digits, or . _ : - characters.",
            },
        )

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    reference = f"GG-{uuid.uuid4().hex[:10].upper()}"
    try:
        with db_connection() as connection:
            if idempotency_key:
                prior = connection.execute(
                    f"SELECT * FROM outage_reports WHERE idempotency_key = {SQL_PARAM}",
                    (idempotency_key,),
                ).fetchone()
                if prior:
                    if prior["service_area"] != area or prior["issue_type"] != issue_type:
                        raise HTTPException(
                            status_code=409,
                            detail={
                                "code": "idempotency_conflict",
                                "message": "This request key was already used for a different report.",
                            },
                        )
                    return OutageReportReceipt(**dict(prior))

            connection.execute(
                f"""
                INSERT INTO outage_reports
                    (reference, service_area, issue_type, created_at, idempotency_key)
                VALUES ({SQL_PARAM}, {SQL_PARAM}, {SQL_PARAM}, {SQL_PARAM}, {SQL_PARAM})
                """,
                (reference, area, issue_type, created_at, idempotency_key),
            )
    except HTTPException:
        raise
    except DB_ERRORS as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "report_store_unavailable",
                "message": "The demonstration report could not be saved. Please retry or use an escalation option.",
            },
        ) from exc

    return OutageReportReceipt(
        reference=reference,
        service_area=area,
        issue_type=issue_type,
        created_at=created_at,
    )


@app.get(
    "/api/v1/outage-reports/{reference}",
    response_model=OutageReportReceipt,
    tags=["demonstration actions"],
    summary="Read a fictional report receipt",
)
def get_outage_report(
    reference: Annotated[str, PathParam(pattern=r"^GG-[A-F0-9]{10}$")],
    authorization: Annotated[str | None, Header()] = None,
) -> OutageReportReceipt:
    require_api_key(authorization)
    require_report_storage()
    try:
        with db_connection() as connection:
            row = connection.execute(
                f"SELECT * FROM outage_reports WHERE reference = {SQL_PARAM}",
                (reference,),
            ).fetchone()
    except DB_ERRORS as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "report_store_unavailable",
                "message": "The demonstration report store is temporarily unavailable.",
            },
        ) from exc
    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "report_not_found",
                "message": "No demonstration report was found for that reference.",
            },
        )
    return OutageReportReceipt(**dict(row))
