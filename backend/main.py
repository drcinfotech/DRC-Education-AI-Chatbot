"""
FastAPI entry point for the Education & EdTech AI Chatbot.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.catalog import catalog
from app.chatbot import engine
from app.models import ChatRequest, ChatResponse
from app.sessions import store

app = FastAPI(
    title="Education AI Chatbot — Study Assistant",
    description=(
        "A demo conversational AI for K-12 and higher-ed students. Includes intent classification, "
        "academic-integrity guardrails, privacy scoping, and rich response blocks for courses, "
        "assignments, grades, attendance, schedule, fees, and tutoring. NOT a substitute for a "
        "real teacher."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "courses":     len(catalog.courses()),
        "assignments": len(catalog.assignments()),
        "concepts":    len(catalog.all_concepts()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = store.get_or_create(req.session_id)
    return engine.respond(req.message, session)


@app.get("/profile")
def get_profile():
    return catalog.profile()


@app.get("/courses")
def list_courses():
    return catalog.courses()


@app.get("/assignments")
def list_assignments():
    return catalog.assignments()


@app.get("/grades")
def list_grades():
    return catalog.grades()


@app.get("/attendance")
def get_attendance():
    return catalog.attendance()


@app.get("/schedule")
def get_schedule():
    return catalog.today_schedule()


@app.get("/fees")
def get_fees():
    return catalog.fees()


@app.get("/concepts")
def list_concepts():
    return catalog.all_concepts()


@app.get("/study-techniques")
def list_study_techniques():
    return catalog.study_techniques()


@app.get("/")
def root():
    return {
        "name":       "Education AI Chatbot — Study Assistant",
        "version":    app.version,
        "docs":       "/docs",
        "disclaimer": "Demo only. Not a substitute for a real teacher.",
    }
