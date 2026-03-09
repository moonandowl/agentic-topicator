"""Agentic Topicator — FastAPI app."""

import io
import re
import zipfile
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from config import get_settings
from models import GenerateBriefsRequest, GenerateTopicsRequest
from services import generate_briefs, generate_topics

app = None  # Set after we have templates


def verify_auth(username: str, password: str, settings) -> bool:
    import secrets

    return secrets.compare_digest(
        username.encode("utf-8"), settings.auth_username.encode("utf-8")
    ) and secrets.compare_digest(
        password.encode("utf-8"), settings.auth_password.encode("utf-8")
    )


def setup_app():
    global app
    from fastapi import FastAPI

    app = FastAPI(title="Agentic Topicator")

    templates_dir = Path(__file__).parent / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/results", response_class=HTMLResponse)
    async def results_page(request: Request):
        return templates.TemplateResponse("results.html", {"request": request})

    @app.get("/briefs", response_class=HTMLResponse)
    async def briefs_page(request: Request):
        return templates.TemplateResponse("briefs.html", {"request": request})

    @app.post("/api/generate-topics")
    async def api_generate_topics(body: GenerateTopicsRequest):
        settings = get_settings()
        api_keys = {
            "anthropic": settings.anthropic_api_key,
            "openai": settings.openai_api_key,
            "google": settings.google_api_key,
            "perplexity": settings.perplexity_api_key,
            "grok": settings.xai_api_key,
        }
        key = api_keys.get(body.model_provider, "")
        if not key:
            raise HTTPException(
                400,
                f"No API key configured for {body.model_provider}. Set the corresponding env var.",
            )
        results = await generate_topics(
            body.topic, body.audience, body.model_provider, settings
        )
        return [r.model_dump() for r in results]

    @app.post("/api/generate-briefs")
    async def api_generate_briefs(body: GenerateBriefsRequest):
        settings = get_settings()
        key_name = body.model_provider
        api_keys = {
            "anthropic": settings.anthropic_api_key,
            "openai": settings.openai_api_key,
            "google": settings.google_api_key,
            "perplexity": settings.perplexity_api_key,
            "grok": settings.xai_api_key,
        }
        if not api_keys.get(key_name, ""):
            raise HTTPException(
                400,
                f"No API key configured for {key_name}. Set the corresponding env var.",
            )
        briefs = await generate_briefs(
            body.selections,
            body.original_topic,
            body.original_audience,
            body.model_provider,
            settings,
        )
        return [b.model_dump() for b in briefs]

    @app.post("/api/export-briefs")
    async def api_export_briefs_post(request: Request):
        body = await request.json()
        briefs_data = body.get("briefs", [])
        if not briefs_data:
            raise HTTPException(400, "briefs array required")

        def slug(s: str) -> str:
            return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-")[:50]

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, b in enumerate(briefs_data):
                sel = b.get("selection", {})
                topic_slug = slug(sel.get("topic", "brief"))
                agent_slug = slug(sel.get("sub_agent_name", "agent"))
                content = b.get("content", "")
                filename = f"{topic_slug}-{agent_slug}-Brief.md"
                if filename in [info.filename for info in zf.infolist()]:
                    filename = f"{topic_slug}-{agent_slug}-{i}-Brief.md"
                zf.writestr(filename, content)

        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=briefs.zip"},
        )

    @app.post("/api/export-single")
    async def api_export_single(request: Request):
        body = await request.json()
        content = body.get("content", "")
        filename = body.get("filename", "brief.md")
        if not content:
            raise HTTPException(400, "content required")
        return StreamingResponse(
            io.BytesIO(content.encode("utf-8")),
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    # Add auth middleware for routes other than /health
    from starlette.middleware.base import BaseHTTPMiddleware

    class AuthMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            if request.url.path == "/health":
                return await call_next(request)
            settings = get_settings()
            if not settings.auth_enabled:
                return await call_next(request)
            auth = request.headers.get("Authorization")
            if auth and auth.startswith("Basic "):
                import base64
                try:
                    decoded = base64.b64decode(auth[6:]).decode()
                    user, passwd = decoded.split(":", 1)
                    if verify_auth(user, passwd, settings):
                        return await call_next(request)
                except Exception:
                    pass
            # For HTML pages, return 401 with WWW-Authenticate
            accept = request.headers.get("Accept", "")
            if "text/html" in accept:
                from starlette.responses import Response
                return Response(
                    content="<h1>Authorization required</h1>",
                    status_code=401,
                    headers={"WWW-Authenticate": "Basic realm='Agentic Topicator'"},
                    media_type="text/html",
                )
            from starlette.responses import JSONResponse
            return JSONResponse(
                {"detail": "Not authenticated"},
                status_code=401,
                headers={"WWW-Authenticate": "Basic realm='Agentic Topicator'"},
            )

    app.add_middleware(AuthMiddleware)

    return app


# Lazy init so we can mount templates
app = setup_app()
