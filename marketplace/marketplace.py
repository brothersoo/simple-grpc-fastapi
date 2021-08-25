import grpc
import os
import uvicorn

from typing import Optional

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from recommendations.recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations.recommendations_pb2_grpc import RecommendationsStub

app = FastAPI()

templates = Jinja2Templates(directory="templates")

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)

@app.get("/")
def render_homepage():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    return templates.TemplateResponse(
        "homepage.html",
        recommendations=recommendations_response.recommendations,
    )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)