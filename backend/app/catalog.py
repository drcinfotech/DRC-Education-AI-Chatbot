"""
Data catalog — loads student record and content from JSON.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


DATA_DIR = Path(__file__).parent.parent / "data"


class Catalog:
    def __init__(self):
        with open(DATA_DIR / "student.json", "r", encoding="utf-8") as f:
            self._student = json.load(f)
        with open(DATA_DIR / "content.json", "r", encoding="utf-8") as f:
            self._content = json.load(f)
        # build course-id → name lookup for resolved blocks
        self._course_name = {c["id"]: c["name"] for c in self._student["courses"]}
        self._course_color = {c["id"]: c["color"] for c in self._student["courses"]}
        self._course_code = {c["id"]: c["code"] for c in self._student["courses"]}

    # ── Student profile & academic record ──────────────
    def profile(self) -> dict:
        return dict(self._student["student"])

    def courses(self) -> list[dict]:
        return list(self._student["courses"])

    def assignments(self) -> list[dict]:
        """Return assignments with course name resolved."""
        return [
            {**a, "course_name": self._course_name.get(a["course"], "Unknown"),
                  "course_color": self._course_color.get(a["course"], "#888"),
                  "course_code": self._course_code.get(a["course"], "")}
            for a in self._student["assignments"]
        ]

    def upcoming_assignments(self, limit: int = 6) -> list[dict]:
        items = [a for a in self.assignments() if a["status"] != "submitted" and a["due_in_hours"] > -24]
        items.sort(key=lambda a: a["due_in_hours"])
        return items[:limit]

    def grades(self) -> list[dict]:
        return [
            {**g, "course_name": self._course_name.get(g["course"], "Unknown"),
                  "course_color": self._course_color.get(g["course"], "#888")}
            for g in self._student["grades_recent"]
        ]

    def attendance(self) -> dict:
        a = dict(self._student["attendance"])
        a["by_course"] = [
            {**bc, "course_name": self._course_name.get(bc["course"], "Unknown"),
                   "course_color": self._course_color.get(bc["course"], "#888")}
            for bc in a["by_course"]
        ]
        return a

    def today_schedule(self) -> list[dict]:
        return list(self._student["today_schedule"])

    def fees(self) -> dict:
        return dict(self._student["fees"])

    # ── Content library ────────────────────────────────
    def concept(self, topic_id: str) -> Optional[dict]:
        for c in self._content["concepts"]:
            if c["id"] == topic_id:
                return c
        return None

    def all_concepts(self) -> list[dict]:
        return list(self._content["concepts"])

    def study_techniques(self) -> list[dict]:
        return list(self._content["study_techniques"])


catalog = Catalog()
