# app/main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import base64, json
import openai

app = FastAPI()

# Load scraped content
with open("app/discourse.json", "r") as f:
    discourse_data = json.load(f)

with open("app/course_content.json", "r") as f:
    course_data = json.load(f)

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None

@app.post("/api/")
async def ask_question(request: QuestionRequest):
    query = request.question.lower()

    # Search relevant discourse posts
    related_links = []
    for post in discourse_data:
        if query.split()[0] in post['content'].lower():
            related_links.append({
                "url": post["url"],
                "text": post["title"]
            })
        if len(related_links) >= 2:
            break

    # Generate answer using OpenAI
    openai.api_key = "your-openai-key-here"  # Use env variable in prod
    prompt = f"Answer this student query:\n{query}\n\nUse TDS Jan 2025 context."

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = res['choices'][0]['message']['content']
    except Exception as e:
        answer = f"Error generating answer: {str(e)}"

    return {
        "answer": answer,
        "links": related_links
    }
