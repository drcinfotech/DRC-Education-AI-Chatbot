# Contributing to Study Assistant

Thanks for your interest! This is a demo of conversational AI for the education / EdTech domain, so contributions are welcome — but **integrity-critical code paths have extra rules** that apply on top of normal code-review.

## Code of conduct

Be kind. Disagree on technical merits, not on people. Maintainers reserve the right to close issues and PRs that violate this.

## Quick start for contributors

```bash
git clone https://github.com/drcinfotech/Education-AI-Chatbot.git
cd Education-AI-Chatbot

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v       # must be 47/47 green before you start

# Frontend
cd ../frontend
npm install
npm run dev
```

## What we accept

✅ **Good contributions:**

- New intents with corresponding tests
- New block renderers in `Blocks.jsx` with corresponding Pydantic models
- New academic-integrity patterns — with both a positive test and a no-false-positive test
- New concept explanations (subject content) in `content.json`
- Documentation, README improvements, screenshots
- Accessibility improvements (keyboard nav, ARIA, contrast)
- i18n / localization support (Hindi, Tamil, Bengali, etc)
- Tighter test coverage

❌ **What we do NOT accept:**

- Real EdTech, school, or learning-platform brand names anywhere in the codebase. The CI test `test_no_real_edtech_brands_in_data` will fail your PR.
- Removing or weakening the academic-integrity layer
- Anything that helps students cheat — writing essays for them, providing test answers, bypassing plagiarism detection
- Making the bot reveal another student's data
- Removing or relaxing prompt-injection / social-engineering blocks
- Adding personal API keys or credentials
- Code that calls real school information systems (SIS) or learning management systems (LMS) without explicit opt-in and clear documentation of risks
- Replacing the generic "Study Assistant" name with an unverified brand name (see the "name policy" note in the main README)

## Integrity-rule changes (require extra review)

Any PR that modifies the following files **must** include test coverage and a written rationale in the PR description:

- `backend/app/safety.py` — academic-integrity, privacy, and social-engineering detection
- `backend/app/chatbot.py` — the "teach instead of do" handlers and disclaimer injection
- `backend/data/*.json` — particularly anything that resembles a real student, school, or brand
- `backend/data/content.json` — subject explanations should be accurate enough to not mislead students

Maintainers will request changes to any integrity-weakening PR unless the justification is strong. When in doubt about whether a request is asking for "help" vs "cheating," the safe default is to **offer to teach** rather than to provide the answer.

## Style

- Python: PEP 8, type hints on public functions, docstrings on modules
- JS/JSX: 2-space indent, prefer functional components, hooks for state
- Commits: imperative present tense ("Add X", "Fix Y"), not past tense
- One logical change per PR

## Reporting a security issue

For anything that looks like a real security issue (not just a demo limitation), please email the maintainers privately rather than opening a public issue.
