import re
from pathlib import Path
from typing import Literal

import ollama
from pydantic import BaseModel, ValidationError

MODEL = "llama3.2"
JOBS_DIR = Path(__file__).parent / "jobs"

SYSTEM_PROMPT = """You are a careful data extraction assistant for a recruitment tool.

Read the job advertisement inside <job> tags and return one JSON object with exactly these six keys:

"title": string or null.
  The job title copied exactly as written, including any detail in brackets, e.g. "Software Engineer (Java)". null if no title is given.

"skills": list of strings.
  Every concrete technology, tool, language, framework, database or engineering practice the ad asks for.
  - Keep each item short (1-4 words).
  - When the ad names specific products, list each one, e.g. "PostgreSQL", "MySQL", not "relational databases".
  - Include engineering practices such as "automated testing" or "CI/CD" when the ad mentions them.
  - Leave out personality traits ("team player") and vague phrases ("modern programming language").
  - No duplicates. Use [] if none are named.

"years_quote": string or null.
  The exact sentence from the ad that states a number of years of experience, copied word for word. null if the ad gives no number of years.

"years_experience": integer or null.
  The minimum number of years stated in years_quote. For a range like "3-5 years" use 3. null if years_quote is null.
  Never infer years from the job title or from words such as "mid" or "senior".

"location": list of strings.
  Only place names written in the ad: cities, regions or countries, e.g. ["Leeds", "Manchester"].
  List every place mentioned for the job. Never put "Remote", "hybrid" or "flexible" here. Use [] if no place is named.

"work_mode": "onsite", "hybrid", "remote" or null.
  How the job is worked, only if the ad says so. If the ad offers a choice, use the most flexible one. null if not stated.

Only use information written in the ad. If something is missing or unclear, use null or [] instead of guessing.

Example 1
<job>
Backend Developer (Python) - Bristol or Cardiff
You will build REST APIs with Python and Django, store data in PostgreSQL and Redis, and deploy with Docker. We value pair programming. You need at least 3 years of Python experience. Hybrid working: two days a week in the office.
</job>
Output:
{"title": "Backend Developer (Python)", "skills": ["Python", "Django", "REST APIs", "PostgreSQL", "Redis", "Docker", "pair programming"], "years_quote": "You need at least 3 years of Python experience.", "years_experience": 3, "location": ["Bristol", "Cardiff"], "work_mode": "hybrid"}

Example 2
<job>
Graduate Engineer
Join our friendly team and help us build great products. Some professional experience is helpful. This is a fully remote role. You are curious, organised and keen to learn.
</job>
Output:
{"title": "Graduate Engineer", "skills": [], "years_quote": null, "years_experience": null, "location": [], "work_mode": "remote"}

Return only the JSON object for the job you are given: no explanation, no greeting and no markdown code fences."""


# The contract: what a valid answer must look like
class Job(BaseModel):
    title: str | None
    skills: list[str]
    years_quote: str | None
    years_experience: int | None
    location: list[str]
    work_mode: Literal["onsite", "hybrid", "remote"] | None


# Layers 1 and 2: the prompt persuades, the schema forces the shape
def extract(job_text: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"<job>\n{job_text}\n</job>"},
        ],
        format=Job.model_json_schema(),
        options={"temperature": 0},
    )
    return response["message"]["content"]


# Flatten spacing and case so the same text matches however it's formatted
def squash(text: str) -> str:
    return " ".join(text.split()).lower()


# Does the quote state this number followed by "year(s)"?
# Accepts "3 years", "3+ years", "3-5 years", "3 to 5 years", "at least 3 years"
def years_supported(quote: str, years: int) -> bool:
    pattern = rf"\b{years}\+?\s*(?:(?:-|–|to)\s*\d+\+?\s*)?years?\b"
    return re.search(pattern, quote.lower()) is not None


# Layer 3: verify the content against the ad and discard what can't be confirmed
def clean_up(job: Job, job_text: str) -> Job:
    ad = squash(job_text)

    # Years: keep only if the quote is really in the ad AND states that number of years
    quote_ok = job.years_quote is not None and squash(job.years_quote) in ad
    years_ok = (
        job.years_experience is not None
        and quote_ok
        and years_supported(job.years_quote, job.years_experience)
    )
    if not years_ok:
        if job.years_experience is not None:
            print(f"(years discarded: {job.years_experience} is not supported by the ad)")
        job.years_quote = None
        job.years_experience = None

    # Skills: keep only skills that actually appear in the ad
    kept = [s for s in job.skills if squash(s) in ad]
    dropped = [s for s in job.skills if s not in kept]
    if dropped:
        print(f"(skills discarded, not found in the ad: {dropped})")
    job.skills = kept

    # Locations: remove blank entries
    job.location = [p for p in job.location if p.strip()]
    return job


for path in sorted(JOBS_DIR.glob("*.txt")):
    job_text = path.read_text(encoding="utf-8")
    raw = extract(job_text)
    print(f"\n=== {path.name} ===")
    try:
        job = clean_up(Job.model_validate_json(raw), job_text)
        print(job.model_dump_json(indent=2))
    except ValidationError as e:
        print("INVALID:\n" + str(e))