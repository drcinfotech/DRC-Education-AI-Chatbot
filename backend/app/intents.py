"""
Intent classifier for the Education & EdTech chatbot.

Safety detection (see safety.py) runs BEFORE this classifier.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentSpec:
    name: str
    patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


INTENTS: list[IntentSpec] = [
    IntentSpec(
        "greeting",
        patterns=[r"^\s*(hi|hello|hey|hola|namaste|good (morning|afternoon|evening))\b"],
        keywords=["hi", "hello", "hey", "hola", "namaste"],
    ),
    IntentSpec(
        "goodbye",
        patterns=[r"\b(bye|goodbye|see ya|see you|cya|take care|gotta go)\b"],
        keywords=["bye", "goodbye"],
    ),
    IntentSpec(
        "thanks",
        patterns=[r"^\s*(thanks|thank you|thx|ty|appreciate it)\b"],
        keywords=["thanks", "thank"],
    ),
    IntentSpec(
        "view_courses",
        patterns=[
            r"\b(show|view|list|all)\s+(my\s+)?(courses|subjects|classes)\b",
            r"\b(what|which)\s+(courses|subjects|classes)\s+(am\s+i\s+taking|do\s+i\s+have)",
            r"\bmy\s+(courses|subjects|classes)\b",
        ],
        keywords=["my courses", "my subjects", "list courses"],
    ),
    IntentSpec(
        "view_assignments",
        patterns=[
            r"\b(show|view|list|all|upcoming|pending)\s+(my\s+)?(assignments|homework|tasks)\b",
            r"\b(what'?s|whats)\s+(due|pending|upcoming)\b",
            r"\bassignments?\s+(due|coming\s+up|this\s+week)\b",
            r"\bmy\s+homework\b",
            r"\bdo\s+i\s+have\s+(any\s+)?(assignments?|homework)\b",
            r"\bwhat\s+do\s+i\s+have\s+to\s+do\b",
        ],
        keywords=["assignments", "homework", "due", "pending"],
    ),
    IntentSpec(
        "view_grades",
        patterns=[
            r"\b(show|view|see|check|my)\s+(my\s+)?(grades?|scores?|marks|results?)\b",
            r"\bhow'?s\s+my\s+(grades?|marks|scores?)\b",
            r"\brecent\s+(grades?|marks|scores?)\b",
            r"\b(report\s+card|gradebook)\b",
            r"\bhow\s+am\s+i\s+doing\s+in\s+(school|class|my\s+(courses|subjects))\b",
        ],
        keywords=["grades", "marks", "scores", "results"],
    ),
    IntentSpec(
        "view_attendance",
        patterns=[
            r"\b(my|view|show|check)\s+attendance\b",
            r"\bhow\s+many\s+(days|classes)\s+have\s+i\s+(missed|attended)\b",
            r"\battendance\s+(percentage|record)\b",
        ],
        keywords=["attendance"],
    ),
    IntentSpec(
        "view_schedule",
        patterns=[
            r"\b(my|today'?s|tomorrow'?s|this\s+week'?s)\s+(schedule|timetable|classes|lessons)\b",
            r"\bwhat\s+(classes|subjects|lessons)\s+do\s+i\s+have\b",
            r"\b(class\s+)?timetable\b",
        ],
        keywords=["schedule", "timetable", "today's classes"],
    ),
    IntentSpec(
        "view_fees",
        patterns=[
            r"\b(my\s+)?(school\s+)?fees?\b",
            r"\b(fee|tuition|payment)\s+(status|breakdown|details|due)",
            r"\bhow\s+much\s+(do\s+i\s+)?owe\b",
            r"\bpending\s+(fee|payment)",
        ],
        keywords=["fees", "tuition", "payment"],
    ),
    IntentSpec(
        "explain_concept",
        patterns=[
            r"\b(explain|teach|tell\s+me\s+about|what\s+is|what\s+are|help\s+me\s+understand)\s+",
            r"\bwhat\s+does\s+\w+\s+mean\b",
            r"\bcan\s+you\s+(explain|teach)\b",
            r"\bi\s+don'?t\s+understand\b",
        ],
        keywords=["explain", "teach", "what is", "help me understand"],
    ),
    IntentSpec(
        "worked_example",
        patterns=[
            r"\b(show|give|walk\s+me\s+through)\s+(me\s+)?(an?\s+)?(example|worked\s+example|sample\s+problem)\b",
            r"\bsolve\s+(a|an|one)\s+(example|practice|sample)\b",
            r"\bstep[\s-]by[\s-]step\s+(example|problem|solution)\b",
        ],
        keywords=["example", "worked example", "step by step"],
    ),
    IntentSpec(
        "study_plan",
        patterns=[
            r"\b(make|create|build|plan)\s+(me\s+)?(a\s+)?study\s+(plan|schedule)\b",
            r"\bhow\s+(should|do)\s+i\s+(study|prepare)\s+for\b",
            r"\bplan\s+my\s+(week|study)\b",
            r"\bstudy\s+schedule\b",
        ],
        keywords=["study plan", "study schedule", "how should I study"],
    ),
    IntentSpec(
        "study_techniques",
        patterns=[
            r"\b(study\s+)?(techniques|methods|tips|strategies)\b",
            r"\bhow\s+to\s+study\s+(better|effectively|smart)",
            r"\b(active\s+recall|spaced\s+repetition|pomodoro|feynman)\b",
            r"\bhow\s+do\s+i\s+memorize\b",
        ],
        keywords=["study techniques", "study tips", "study methods"],
    ),
    IntentSpec(
        "flashcards",
        patterns=[
            r"\b(make|create|generate)\s+(me\s+)?flashcards?\b",
            r"\bquiz\s+me\s+on\b",
            r"\btest\s+(me\s+on|my\s+knowledge\s+of)\b",
            r"\bpractice\s+questions?\b",
        ],
        keywords=["flashcards", "quiz me", "practice questions"],
    ),
    IntentSpec(
        "profile",
        patterns=[
            r"\b(my|view|show)\s+(profile|account|details|information)\b",
            r"\bwho\s+am\s+i\b",
            r"\bmy\s+(student\s+)?id\b",
        ],
        keywords=["my profile", "my account"],
    ),
    IntentSpec(
        "talk_to_teacher",
        patterns=[
            r"\b(speak|talk|connect|message)\s+(to\s+)?(a\s+)?(teacher|tutor|counsellor|counselor|advisor)\b",
            r"\b(real|human|live)\s+(teacher|tutor|advisor)\b",
            r"\bcontact\s+(my\s+)?teacher\b",
        ],
        keywords=["teacher", "tutor", "human help"],
    ),
]


# ─── Subject extraction ────────────────────────────────────
SUBJECTS = {
    "physics":           ["physics", "phy", "kinematics", "motion", "force", "newton", "gravity", "energy", "wave"],
    "mathematics":       ["math", "maths", "mathematics", "trig", "trigonometry", "algebra", "calculus", "geometry", "sets", "relations", "function"],
    "chemistry":         ["chemistry", "chem", "bonding", "reaction", "acid", "base", "organic", "inorganic", "salt"],
    "biology":           ["biology", "bio", "cell", "respiration", "photosynthesis", "evolution", "genetics", "mitosis", "meiosis"],
    "english":           ["english", "essay", "hamlet", "literature", "poem", "comprehension", "grammar"],
    "computer_science":  ["computer science", "cs", "python", "loop", "function", "list", "dict", "java", "programming", "algorithm"],
}

TOPIC_KEYWORDS = {
    "phy-kinematics":      ["kinematics", "motion", "displacement", "velocity", "acceleration", "projectile"],
    "math-trigonometry":   ["trigonometry", "trig", "sin", "cos", "tan", "identity", "identities", "sine", "cosine"],
    "chem-bonding":        ["bonding", "bond", "ionic", "covalent", "electronegativity"],
    "bio-cell-respiration": ["respiration", "atp", "glycolysis", "krebs", "mitochondria", "fermentation"],
    "cs-python-loops":     ["loop", "loops", "for loop", "while loop", "iteration", "range", "python"],
}


def extract_subject(text: str) -> Optional[str]:
    t = text.lower()
    for key, words in SUBJECTS.items():
        if any(w in t for w in words):
            return key
    return None


def extract_topic_id(text: str) -> Optional[str]:
    t = text.lower()
    # score by number of keyword matches; pick the topic with most
    scores = {}
    for topic_id, words in TOPIC_KEYWORDS.items():
        score = sum(1 for w in words if w in t)
        if score:
            scores[topic_id] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


# ─── Classifier ────────────────────────────────────────────
@dataclass
class Classification:
    intent: str
    confidence: float
    entities: dict


def classify(text: str) -> Classification:
    raw = text
    text_lc = text.lower().strip()

    scores: dict[str, float] = {}
    for spec in INTENTS:
        score = 0.0
        for p in spec.patterns:
            if re.search(p, text_lc, re.IGNORECASE):
                score += 2.0
        for kw in spec.keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lc):
                score += 0.6
        if score > 0:
            scores[spec.name] = score

    if not scores:
        intent, conf = "unknown", 0.0
    else:
        intent = max(scores, key=scores.get)
        top = scores[intent]
        rest = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0.1
        conf = min(1.0, top / (top + rest))

    entities = {
        "subject":  extract_subject(raw),
        "topic_id": extract_topic_id(raw),
    }
    return Classification(intent=intent, confidence=round(conf, 2), entities=entities)
