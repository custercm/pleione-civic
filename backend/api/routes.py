from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..models.llm_connector import generate_code_and_tests, auto_implement_code, list_project_files
from ..models.safe_update import safe_self_update

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    files_to_include: Optional[List[str]] = None

class ImplementRequest(BaseModel):
    sandbox_files: list
    test_results: dict

class SelfUpdateRequest(BaseModel):
    files_to_update: dict  # {file_path: new_content}

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = generate_code_and_tests(request.prompt, files_to_include=request.files_to_include)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/implement")
async def implement_endpoint(request: ImplementRequest):
    """Automatically implement code that has passed tests"""
    try:
        result = auto_implement_code(request.sandbox_files, request.test_results)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/self-update")
async def self_update_endpoint(request: SelfUpdateRequest):
    """Safely update Pleione's own code with comprehensive testing"""
    try:
        result = safe_self_update(request.files_to_update)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def list_files_endpoint():
    """List all files in the project for context selection"""
    try:
        files = list_project_files(".", extensions=[".py", ".js", ".html", ".css", ".md", ".sh"])
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))