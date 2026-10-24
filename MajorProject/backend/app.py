"""FastAPI application factory and gateway configuration."""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from analyzer.routes import router as analyzer_router
from carbon.routes import router as carbon_router
from config import APP_NAME, APP_VERSION, CORS_ORIGINS, IS_PRODUCTION
from optimizer.routes import router as optimizer_router
from recommendation.routes import router as recommendation_router
from routes.health import router as health_router
from routes.process import router as process_router
from utils.errors import build_error_response
from utils.logging import log_request_event, setup_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        logger.info("Starting %s v%s", APP_NAME, APP_VERSION)
        yield
        logger.info("Shutting down %s", APP_NAME)

    application = FastAPI(
        title=APP_NAME,
        description="Green AI and Sustainable Prompt Engineering System",
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    allow_origins = CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def request_timing_middleware(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Processing-Time-Ms"] = f"{elapsed_ms:.2f}"
        log_request_event(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            processing_time_ms=elapsed_ms,
        )
        return response

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        message = "Internal server error."
        details = None if IS_PRODUCTION else str(exc)
        return build_error_response(message, status_code=500, details=details)

    application.include_router(analyzer_router)
    application.include_router(carbon_router)
    application.include_router(optimizer_router)
    application.include_router(recommendation_router)
    application.include_router(process_router)
    application.include_router(health_router)

    return application


app = create_app()
