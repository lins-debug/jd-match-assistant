"""FastAPI 服务：暴露 /match 接口。"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

from analyzer import analyze


class MatchRequest(BaseModel):
    resume: str
    jd: str
    jd_label: str = ""  # 可选的 JD 标签，用于对比


class MatchResponse(BaseModel):
    report: dict


app = FastAPI(title="简历与 JD 匹配助手")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.post("/match", response_model=MatchResponse)
def match(req: MatchRequest):
    report = analyze(req.resume, req.jd)
    return MatchResponse(report=report)


app.mount("/", StaticFiles(directory=str(ROOT / "static"), html=True), name="static")