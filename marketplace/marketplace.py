import grpc
import logging
import os
import uvicorn

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from google.protobuf.json_format import MessageToDict

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = FastAPI()

templates = Jinja2Templates(directory="templates")

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")

recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051",
    options=(('grpc.enable_http_proxy', 0),)
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.get("/", response_class=HTMLResponse)
async def render_homepage(request: Request):
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    dict_response = MessageToDict(recommendations_response)
    dict_response['request'] = request
    return templates.TemplateResponse(
        "homepage.html",
        dict_response,
    )


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)

