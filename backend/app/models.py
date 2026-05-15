"""
Pydantic models for the Education & EdTech chatbot.
"""
from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


# ─── Request ───────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


# ─── Domain entities ───────────────────────────────────────
class Course(BaseModel):
    id: str
    code: str
    name: str
    teacher: str
    schedule: str
    credits: int
    grade_so_far: str
    color: str


class Assignment(BaseModel):
    id: str
    course: str
    title: str
    due: str
    due_in_hours: int
    status: Literal["not_started", "in_progress", "draft", "submitted", "graded"]
    points: int
    type: str


class GradeEntry(BaseModel):
    id: str
    course: str
    title: str
    score: int
    max: int
    pct: int
    letter: str
    date: str


class AttendanceByCourse(BaseModel):
    course: str
    pct: float


class ScheduleSlot(BaseModel):
    time: str
    course: Optional[str] = None
    name: str
    room: str
    teacher: str
    note: str


class FeeBreakdownItem(BaseModel):
    head: str
    amount: int
    paid: int


class WorkedExampleStep(BaseModel):
    problem: str
    steps: list[str]
    answer: str


class ConceptFormula(BaseModel):
    label: str
    formula: str


class StudyTechnique(BaseModel):
    id: str
    name: str
    description: str
    best_for: str


# ─── Rich message blocks ───────────────────────────────────
class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    content: str


class DisclaimerBlock(BaseModel):
    type: Literal["disclaimer"] = "disclaimer"
    content: str


class IntegrityAlertBlock(BaseModel):
    type: Literal["integrity_alert"] = "integrity_alert"
    headline: str
    message: str
    indicators: list[str]
    offer: str   # what we CAN do instead


class CoursesBlock(BaseModel):
    type: Literal["courses"] = "courses"
    title: Optional[str] = None
    items: list[Course]


class AssignmentsBlock(BaseModel):
    type: Literal["assignments"] = "assignments"
    title: Optional[str] = None
    items: list[dict]   # course name resolved server-side


class GradesBlock(BaseModel):
    type: Literal["grades"] = "grades"
    title: Optional[str] = None
    items: list[dict]
    average_pct: float


class AttendanceBlock(BaseModel):
    type: Literal["attendance"] = "attendance"
    overall_pct: float
    present_days: int
    total_days: int
    by_course: list[dict]   # name resolved


class ScheduleBlock(BaseModel):
    type: Literal["schedule"] = "schedule"
    title: Optional[str] = None
    items: list[ScheduleSlot]


class FeesBlock(BaseModel):
    type: Literal["fees"] = "fees"
    term: str
    total: int
    paid: int
    due: int
    due_date: str
    breakdown: list[FeeBreakdownItem]


class ConceptBlock(BaseModel):
    type: Literal["concept"] = "concept"
    subject: str
    topic: str
    summary: str
    key_formulas: list[ConceptFormula]
    common_mistakes: list[str]
    next_topics: list[str]


class WorkedExampleBlock(BaseModel):
    type: Literal["worked_example"] = "worked_example"
    topic: str
    problem: str
    steps: list[str]
    answer: str


class StudyPlanBlock(BaseModel):
    type: Literal["study_plan"] = "study_plan"
    title: str
    horizon: str
    sessions: list[dict]   # [{day, blocks: [{subject, topic, duration_min, technique}]}]


class StudyTechniquesBlock(BaseModel):
    type: Literal["study_techniques"] = "study_techniques"
    title: Optional[str] = None
    items: list[StudyTechnique]


class ProfileBlock(BaseModel):
    type: Literal["profile"] = "profile"
    student: dict


class FlashcardsBlock(BaseModel):
    type: Literal["flashcards"] = "flashcards"
    topic: str
    cards: list[dict]   # [{front, back}]


MessageBlock = (
    TextBlock | DisclaimerBlock | IntegrityAlertBlock
    | CoursesBlock | AssignmentsBlock | GradesBlock | AttendanceBlock
    | ScheduleBlock | FeesBlock | ConceptBlock | WorkedExampleBlock
    | StudyPlanBlock | StudyTechniquesBlock | ProfileBlock | FlashcardsBlock
)


# ─── Response ──────────────────────────────────────────────
class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    blocks: list[MessageBlock]
    suggestions: list[str] = []
    safety_flag: Optional[str] = None   # None | "academic_integrity" | "privacy" | "social_engineering"
