ROUND 01 - """Extract the job title, skills, years of experience and location from the job ad.""" -> prose instead of JSON, differnt format and output for each job, inconsistent skill recognition, hallusination for the years of experience block(guessed blindly).

ROUND 2 - 
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

OUTPUT - === job2.txt ===
(years discarded: 8 is not supported by the ad)
{
  "title": "Mid Software Engineer (Java)",
  "skills": [
    "Java",
    "Spring Boot",
    "Streams",
    "Lambdas",
    "Optional",
    "REST API design",
    "PostgreSQL",
    "MySQL",
    "SQL Server",
    "automated testing",
    "Git",
    "CI/CD"
  ],
  "years_quote": null,
  "years_experience": null,
  "location": [
    "Edinburgh",
    "Leeds",
    "Manchester",
    "London",
    "Bulgaria"
  ],
  "work_mode": "hybrid"
}

=== job3.txt ===
{
  "title": "Java Developer",
  "skills": [
    "Java",
    "Oracle database"
  ],
  "years_quote": null,
  "years_experience": null,
  "location": [
    "Nottingham"
  ],
  "work_mode": "hybrid"
}

Improvement after round2 - Added schema enforcement and code checks. Caught Java 8+ → 8 years, invented 0, leaked ‘pair programming’ and empty location. Remaining: MongoDB and DynamoDB missed (recall).