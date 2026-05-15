"""
Academic-integrity & privacy guardrails — runs BEFORE intent classification.

In an education chatbot, the gravest harms are:
  • Doing the student's graded work FOR them (cheating)
  • Exposing one student's data to another (privacy)
  • Being tricked into bypassing rules (social engineering / prompt injection)

This module catches these and short-circuits to a friendly refusal that
offers an honest alternative — teach the concept instead of doing the work.

Conservative by design — when in doubt, we offer to teach rather than to do.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SafetyResult:
    flag: Optional[Literal["academic_integrity", "privacy", "social_engineering"]]
    reason: str = ""


# ─── Academic integrity patterns ───────────────────────────
# Catch requests to actually DO the graded work, not learn from it.
ACADEMIC_INTEGRITY_PATTERNS = [
    # "Write my X for me" style
    r"\b(write|do|complete|finish|solve)\s+(my|the)\s+(\w+\s+){0,3}(essay|paper|assignment|homework|coursework|report|project|lab\s+report|thesis|test|exam|quiz|midterm|final)\b",
    r"\bdo\s+my\s+(homework|assignment|essay|project)\b",

    # "Give me the answers"
    r"\b(give|tell|show)\s+me\s+(the\s+)?(answers?|solutions?)\s+(to|for)\s+(my|the|this)\s+(\w+\s+){0,2}(test|exam|quiz|assignment|homework)",
    r"\banswer\s+key\s+(for|to)\s+(my|the|this)\b",
    r"\b(test|exam|quiz)\s+answers?\b",

    # Take an exam / test for me
    r"\b(take|sit|write|do)\s+(my|the)\s+(test|exam|quiz|midterm|final)\s+(for me)?",
    r"\b(help|do)\s+me\s+cheat\s+on\b",
    r"\bcheat\s+on\s+(my|the|this)\s+(test|exam|quiz|assignment)\b",

    # Write a full essay / Code my entire project
    r"\bwrite\s+(me\s+)?(a|the|an?)\s+\d*\s*(word|page)?\s*(essay|paper|report|article)\s+(on|about)",
    r"\bwrite\s+(me\s+)?(my|the)\s+\d*\s*word\s+(essay|paper|report)",
    r"\bcode\s+(my|the|this|my\s+entire|the\s+entire|this\s+entire)\s+(project|assignment|program|homework)\b",
    r"\b(code|build|make|do)\s+(my|the)\s+(entire|whole|full|complete)\s+(project|assignment|program|homework)\b",
    r"\bwrite\s+(the\s+)?(whole|entire|full|complete)\s+(code|program|project)\s+for\s+(my|the|this)\s+(assignment|project|homework)",

    # Plagiarism / submission help
    r"\b(paraphrase|rewrite)\s+(this|the\s+following)\s+so\s+(it|i)\s+(won'?t|don'?t|do\s+not)\s+get\s+(caught|flagged|detected)\b",
    r"\bbypass\s+(plagiarism|turnitin|ai\s+detect)",
    r"\bavoid\s+(plagiarism|turnitin|ai\s+detect)\w*",
    r"\b(make|write)\s+(this|it)\s+sound\s+(like|as if)\s+(a\s+)?(human|student)\s+wrote",
]


# ─── Privacy patterns (other students' data) ───────────────
PRIVACY_PATTERNS = [
    # show/tell me about someone else's data — with or without "me", with or without possessive 's
    r"\b(show|tell|give|view|see|check)\s+(me\s+)?(another|other|someone\s+else'?s?|my\s+(friend|friends|classmate|classmates|sister|brother|roommate)'?s?)\s+(grade|score|marks|attendance|fees|record|result)",
    r"\b(what|whats|what'?s)\s+(is\s+)?(\w+\s+)?(my\s+)?(friend|friends|classmate|classmates|sister|brother|roommate)'?s?\s+(grade|score|marks|attendance|fees|record|result)",
    r"\b(tell|show|give)\s+me\s+(my\s+)?(friend|friends|classmate|classmates|sister|brother|roommate)'?s?\s+(grade|score|marks|attendance|fees|record|result)",
    r"\blook\s+up\s+(student\s+|roll\s+(number\s+)?)[\w\d-]+",
    r"\b(grade|score|marks)\s+(of|for)\s+(another\s+student|student\s+\w+|roll\s+number)",
]


# ─── Prompt injection / social engineering ─────────────────
SOCIAL_ENGINEERING_PATTERNS = [
    r"\b(ignore|disregard|forget)\s+(\w+\s+){0,4}(instructions|rules|guidelines|system\s+prompt)",
    r"\byou\s+are\s+now\s+(in\s+|an?\s+)?(admin|administrator|dev|developer|debug|root|teacher|principal)\s+(mode|user)?",
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(admin|root|developer|teacher|principal|examiner)\b",
    r"\b(give|provide|reveal|show|tell)\s+(me\s+)?(your\s+)?(system\s+prompt|instructions|api\s+key|source\s+code)",
    r"\benable\s+(developer|admin|debug|root|teacher)\s+mode\b",
    r"\bjailbreak\b",
    r"\bDAN\s+mode\b",
    r"\bact\s+as\s+(if\s+)?(you\s+have\s+)?no\s+(rules|restrictions|guidelines)",
]


def check_safety(text: str) -> SafetyResult:
    t = text.lower()

    for pat in SOCIAL_ENGINEERING_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="social_engineering", reason=pat)

    for pat in PRIVACY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="privacy", reason=pat)

    for pat in ACADEMIC_INTEGRITY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="academic_integrity", reason=pat)

    return SafetyResult(flag=None)


def build_academic_integrity_block() -> dict:
    return {
        "type": "integrity_alert",
        "headline": "I can't do your graded work for you.",
        "message": (
            "Writing your essay, solving your homework, or taking your test for you would short-circuit "
            "the learning — and at most schools it counts as academic misconduct. I won't do that. "
            "But I'm genuinely good at helping you learn the material so you can do it yourself."
        ),
        "indicators": [
            "Submitting AI-generated work as your own is a violation at most CBSE, ICSE, IB, and Cambridge schools",
            "Many institutions now use AI-detection tools — getting caught has real consequences",
            "Even when 'help' feels harmless, learning happens when YOU do the thinking",
        ],
        "offer": (
            "Here's what I can do: explain the concept, walk through a similar example step-by-step, "
            "quiz you to test understanding, review your own draft, or build a study plan. Want me to start there?"
        ),
    }


def build_privacy_block() -> dict:
    return {
        "type": "integrity_alert",
        "headline": "I can only access your own academic record.",
        "message": (
            "I can't share another student's grades, attendance, fees, or any personal data. "
            "That information belongs to them, and protecting it is non-negotiable."
        ),
        "indicators": [
            "Each student account only sees their own data",
            "School policies and data-protection laws (DPDP Act in India) require this scoping",
            "If you need information about another student, ask them directly or speak to the class teacher",
        ],
        "offer": "I'm happy to help you with your own academic work — grades, schedule, study planning, or tutoring.",
    }


def build_social_engineering_block() -> dict:
    return {
        "type": "integrity_alert",
        "headline": "I can't do that.",
        "message": (
            "I'm not able to bypass my safety rules, switch into a 'teacher mode' that has different "
            "permissions, or reveal internal instructions. If you have a real academic need, "
            "I'm happy to help with that instead."
        ),
        "indicators": [
            "I work the same way for everyone — there's no admin mode to unlock",
            "Real teachers can update your record, give exam access, etc. — I cannot",
            "If you think the system isn't doing what it should, message your class teacher",
        ],
        "offer": "Try asking about your schedule, an assignment, or a concept you want to understand better.",
    }
