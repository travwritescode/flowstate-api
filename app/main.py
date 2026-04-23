from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, tasks

app = FastAPI(
    title="FlowState API",
    description="A task manager API — built as a test automation target.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok"}
