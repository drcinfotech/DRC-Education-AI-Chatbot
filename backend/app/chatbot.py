"""
Education chatbot engine.

Flow:
  1. Safety check first — academic-integrity, privacy, social-engineering
  2. Otherwise, classify intent
  3. Dispatch to handler
  4. Return rich blocks

The engine NEVER:
  • Writes the student's essay / homework / project FOR them
  • Reveals another student's data
  • Provides "the answer" to graded work
  • Acts on social-engineering attempts

The engine ALWAYS:
  • Teaches instead of doing — explains, walks through worked examples, quizzes
  • Scopes to the logged-in student only
  • Encourages teachers for things beyond its scope
"""
from __future__ import annotations

from .catalog import catalog
from .intents import Classification, classify
from .safety import (
    check_safety,
    build_academic_integrity_block,
    build_privacy_block,
    build_social_engineering_block,
)
from .sessions import Session


# ─── Block builders ────────────────────────────────────────
def _text(content: str) -> dict:
    return {"type": "text", "content": content}


def _disclaimer(content: str) -> dict:
    return {"type": "disclaimer", "content": content}


# ─── Intent handlers ───────────────────────────────────────
def _handle_greeting(_s: Session):
    p = catalog.profile()
    return [
        _text(
            f"Hi {p['name'].split()[0]} 👋 — I'm your Study Assistant. I can show you your courses, "
            "assignments, grades, schedule, and fees, or help you actually learn the material — "
            "explanations, worked examples, study plans, and flashcards. What would you like to do?"
        )
    ], ["What's due this week?", "Today's schedule", "Explain a concept", "Make a study plan"]


def _handle_goodbye(_s: Session):
    return [_text("All the best with your studies. Come back anytime.")], []


def _handle_thanks(_s: Session):
    return [_text("You're welcome! Anything else I can help you learn today?")], \
           ["Show my grades", "Upcoming assignments", "Explain a topic"]


def _handle_view_courses(_c: Classification, _s: Session):
    courses = catalog.courses()
    return [
        _text(f"You're taking **{len(courses)} courses** this term. Here's the overview:"),
        {"type": "courses", "title": "Your courses", "items": courses},
    ], ["Today's schedule", "How are my grades?", "Upcoming assignments"]


def _handle_view_assignments(_c: Classification, _s: Session):
    items = catalog.upcoming_assignments(limit=6)
    overdue = [a for a in items if a["due_in_hours"] < 0]
    due_soon = [a for a in items if 0 <= a["due_in_hours"] <= 48]
    intro = (
        f"You have **{len(items)} upcoming assignments**."
        + (f" ⚠️ {len(overdue)} overdue." if overdue else "")
        + (f" {len(due_soon)} due in the next 48 hours." if due_soon else "")
    )
    return [
        _text(intro),
        {"type": "assignments", "title": "Upcoming work", "items": items},
    ], ["Make a study plan", "Explain a concept", "Show my grades"]


def _handle_view_grades(_c: Classification, _s: Session):
    grades = catalog.grades()
    avg = sum(g["pct"] for g in grades) / len(grades) if grades else 0
    profile = catalog.profile()
    return [
        _text(
            f"Your **GPA so far is {profile['gpa']}** out of 10, "
            f"with an average of **{avg:.1f}%** across recent assessments. Here are your latest results:"
        ),
        {"type": "grades", "title": "Recent results", "items": grades, "average_pct": round(avg, 1)},
        _disclaimer(
            "These are recent assessment scores, not your final grade. Final grades are determined by your school "
            "and reflected in your official report card at term-end."
        ),
    ], ["Show attendance", "Where am I struggling?", "Study plan for weakest subject"]


def _handle_view_attendance(_c: Classification, _s: Session):
    a = catalog.attendance()
    status = "excellent" if a["overall_pct"] >= 90 else ("good" if a["overall_pct"] >= 80 else "needs attention")
    return [
        _text(
            f"Your attendance this term is **{a['overall_pct']}%** ({a['present_days']} of "
            f"{a['total_days']} days). That's **{status}**."
        ),
        {"type": "attendance", **a},
    ], ["Today's schedule", "My courses", "Talk to a teacher"]


def _handle_view_schedule(_c: Classification, _s: Session):
    items = catalog.today_schedule()
    return [
        _text(f"Here's your schedule for today — **{len(items)} slots**:"),
        {"type": "schedule", "title": "Today", "items": items},
    ], ["What's due tomorrow?", "Make a study plan", "Show my courses"]


def _handle_view_fees(_c: Classification, _s: Session):
    f = catalog.fees()
    pct = (f["paid"] / f["total"]) * 100 if f["total"] else 0
    return [
        _text(
            f"For **{f['term']}**: ₹{f['paid']:,} paid of ₹{f['total']:,} ({pct:.0f}%). "
            f"**₹{f['due']:,} due by {f['due_date']}.**"
        ),
        {"type": "fees", **f},
        _disclaimer(
            "Fee figures are pulled from the school finance office. For payment confirmations, "
            "receipts, or hardship requests, contact the accounts department directly."
        ),
    ], ["Payment options", "Download receipt", "Talk to accounts"]


def _handle_explain_concept(c: Classification, s: Session):
    topic_id = c.entities.get("topic_id")
    if not topic_id:
        return [_text(
            "Sure — I can explain a concept. Could you tell me which one? For example: "
            "*'Explain kinematics'* or *'What are trigonometric identities?'* or *'Teach me Python loops'.*"
        )], ["Explain kinematics", "Trigonometric identities", "Chemical bonding", "Python loops"]

    concept = catalog.concept(topic_id)
    if not concept:
        return [_text(
            "I have explanations for kinematics, trigonometric identities, chemical bonding, "
            "cellular respiration, and Python loops. Want me to cover one of those?"
        )], ["Kinematics", "Trig identities", "Bonding", "Cell respiration", "Python loops"]

    s.last_topic_id = topic_id
    blocks = [
        _text(f"Let's break down **{concept['topic']}** ({concept['subject']}):"),
        {
            "type": "concept",
            "subject":         concept["subject"],
            "topic":           concept["topic"],
            "summary":         concept["summary"],
            "key_formulas":    concept["key_formulas"],
            "common_mistakes": concept["common_mistakes"],
            "next_topics":     concept["next_topics"],
        },
    ]
    return blocks, ["Show me a worked example", "Quiz me on this", "Common mistakes again", "What's the next topic?"]


def _handle_worked_example(c: Classification, s: Session):
    topic_id = c.entities.get("topic_id") or s.last_topic_id
    if not topic_id:
        return [_text(
            "Happy to walk through a worked example. Which topic? Kinematics, trig identities, bonding, "
            "cell respiration, or Python loops?"
        )], ["Kinematics", "Trig identities", "Bonding", "Cell respiration", "Python loops"]

    concept = catalog.concept(topic_id)
    if not concept:
        return [_text("I don't have a worked example for that one yet. Try kinematics, trig, bonding, respiration, or Python loops.")], []

    we = concept["worked_example"]
    s.last_topic_id = topic_id
    return [
        _text(f"Here's a worked example on **{concept['topic']}**. Try it yourself first, then check your work against mine:"),
        {
            "type": "worked_example",
            "topic":   concept["topic"],
            "problem": we["problem"],
            "steps":   we["steps"],
            "answer":  we["answer"],
        },
    ], ["Explain this concept again", "Quiz me", "Show me a harder example", "Next topic"]


def _handle_study_plan(c: Classification, s: Session):
    # Build a 5-day plan focused on upcoming assignments
    upcoming = catalog.upcoming_assignments(limit=5)
    sessions_plan = []
    days = ["Today", "Tomorrow", "Day 3", "Day 4", "Day 5"]
    techs = ["Active recall", "Pomodoro × 4", "Feynman technique", "Interleaving", "Spaced review"]
    for i, day in enumerate(days):
        blocks = []
        if i < len(upcoming):
            a = upcoming[i]
            blocks.append({
                "subject":     a["course_name"],
                "topic":       a["title"],
                "duration_min": 60 + (i * 10),
                "technique":   techs[i],
            })
        # Add a review block for variety
        if i % 2 == 0 and len(upcoming) > 1:
            other = upcoming[(i + 1) % len(upcoming)]
            blocks.append({
                "subject":     other["course_name"],
                "topic":       "Review notes",
                "duration_min": 30,
                "technique":   "Spaced repetition",
            })
        if blocks:
            sessions_plan.append({"day": day, "blocks": blocks})

    return [
        _text(
            "Here's a **5-day study plan** built around your upcoming assignments. "
            "It mixes deep work with shorter review blocks — and uses different techniques to keep it engaging:"
        ),
        {
            "type":     "study_plan",
            "title":    "Your next 5 days",
            "horizon":  "5 days",
            "sessions": sessions_plan,
        },
        _disclaimer(
            "This is a starter plan based on your due dates. Adjust durations to match your energy levels "
            "and actual exam dates. Consistent shorter sessions beat occasional long ones."
        ),
    ], ["Tell me about Pomodoro", "Active recall explained", "Make flashcards instead", "More study tips"]


def _handle_study_techniques(_c: Classification, _s: Session):
    techs = catalog.study_techniques()
    return [
        _text(
            "Here are five evidence-based study techniques. Each one works best in a specific situation — "
            "the trick is matching the technique to what you're studying:"
        ),
        {"type": "study_techniques", "title": "Proven study techniques", "items": techs},
    ], ["Make me a study plan", "Quiz me on something", "Make flashcards"]


def _handle_flashcards(c: Classification, s: Session):
    topic_id = c.entities.get("topic_id") or s.last_topic_id
    concept = catalog.concept(topic_id) if topic_id else None
    if not concept:
        return [_text(
            "Sure! Which topic should I make flashcards for? I have content on kinematics, trig identities, "
            "bonding, cellular respiration, and Python loops."
        )], ["Kinematics", "Trig identities", "Bonding", "Cell respiration", "Python loops"]

    # Build flashcards from formulas + common mistakes
    cards = []
    for f in concept["key_formulas"]:
        cards.append({"front": f["label"], "back": f["formula"]})
    for i, m in enumerate(concept["common_mistakes"], 1):
        cards.append({"front": f"Common mistake #{i}", "back": m})
    cards.append({"front": "What's a typical exam question?",
                  "back":  concept["worked_example"]["problem"]})
    return [
        _text(f"I've made **{len(cards)} flashcards** for {concept['topic']}. Cover the back, try to recall, then check:"),
        {"type": "flashcards", "topic": concept["topic"], "cards": cards},
    ], ["Show worked example", "Explain again", "Quiz me harder", "Next topic"]


def _handle_profile(_c: Classification, _s: Session):
    return [
        _text("Here's your student profile:"),
        {"type": "profile", "student": catalog.profile()},
    ], ["My courses", "My grades", "My schedule", "My attendance"]


def _handle_talk_to_teacher(_c: Classification, _s: Session):
    return [_text(
        "Sure — I can suggest the right person to reach out to. For specific subjects you can email your "
        "course teacher directly (their details are in your courses view). For broader concerns — "
        "stress, study balance, or things going on at home — your class teacher or school counsellor is a "
        "good first stop."
    )], ["Show my courses", "Mental health resources", "Email my class teacher"]


def _handle_unknown(_c: Classification, _s: Session):
    return [_text(
        "I'm not sure I caught that. I can help with your courses, assignments, grades, attendance, "
        "schedule, fees, or actually teach you a topic. Try one of the buttons below."
    )], ["My assignments", "Today's schedule", "Explain a concept", "Make a study plan"]


# ─── Engine ────────────────────────────────────────────────
class ChatbotEngine:
    def respond(self, message: str, session: Session) -> dict:
        # 1️⃣ Safety check first
        safety = check_safety(message)
        if safety.flag == "academic_integrity":
            return {
                "session_id":   session.session_id,
                "intent":       "academic_integrity_block",
                "confidence":   1.0,
                "blocks":       [build_academic_integrity_block()],
                "suggestions":  ["Explain the concept instead", "Walk me through an example", "Quiz me", "Review my draft"],
                "safety_flag":  "academic_integrity",
            }
        if safety.flag == "privacy":
            return {
                "session_id":   session.session_id,
                "intent":       "privacy_block",
                "confidence":   1.0,
                "blocks":       [build_privacy_block()],
                "suggestions":  ["Show my own grades", "My schedule", "My assignments"],
                "safety_flag":  "privacy",
            }
        if safety.flag == "social_engineering":
            return {
                "session_id":   session.session_id,
                "intent":       "social_engineering_blocked",
                "confidence":   1.0,
                "blocks":       [build_social_engineering_block()],
                "suggestions":  ["Show my schedule", "My assignments", "Explain a concept"],
                "safety_flag":  "social_engineering",
            }

        # 2️⃣ Classify intent
        c = classify(message)
        session.last_intent = c.intent
        session.history.append({"role": "user", "text": message})

        handler_map = {
            "greeting":          lambda: _handle_greeting(session),
            "goodbye":           lambda: _handle_goodbye(session),
            "thanks":            lambda: _handle_thanks(session),
            "view_courses":      lambda: _handle_view_courses(c, session),
            "view_assignments":  lambda: _handle_view_assignments(c, session),
            "view_grades":       lambda: _handle_view_grades(c, session),
            "view_attendance":   lambda: _handle_view_attendance(c, session),
            "view_schedule":     lambda: _handle_view_schedule(c, session),
            "view_fees":         lambda: _handle_view_fees(c, session),
            "explain_concept":   lambda: _handle_explain_concept(c, session),
            "worked_example":    lambda: _handle_worked_example(c, session),
            "study_plan":        lambda: _handle_study_plan(c, session),
            "study_techniques":  lambda: _handle_study_techniques(c, session),
            "flashcards":        lambda: _handle_flashcards(c, session),
            "profile":           lambda: _handle_profile(c, session),
            "talk_to_teacher":   lambda: _handle_talk_to_teacher(c, session),
        }
        handler = handler_map.get(c.intent, lambda: _handle_unknown(c, session))
        blocks, suggestions = handler()

        bot_text = " | ".join(b.get("content", "") for b in blocks if b.get("type") == "text")
        session.history.append({"role": "bot", "text": bot_text})

        return {
            "session_id":   session.session_id,
            "intent":       c.intent,
            "confidence":   c.confidence,
            "blocks":       blocks,
            "suggestions":  suggestions,
            "safety_flag":  None,
        }


engine = ChatbotEngine()
