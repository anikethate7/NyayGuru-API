from fastapi import APIRouter, Depends, HTTPException, Path
from uuid import uuid4

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chatbot import get_chat_response
from app.dependencies import get_retriever, get_llm, get_conversation_memory
from app.config import settings

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    retriever = Depends(get_retriever),
    llm = Depends(get_llm)
):
    """
    Process a chat request and return a response.
    
    - **query**: User's question
    - **category**: Legal category
    - **language**: Response language (default: English)
    - **session_id**: Unique session identifier
    - **messages**: Previous messages in the conversation (optional)
    """
    try:
        # Get or create conversation memory for this session
        memory = get_conversation_memory(request.session_id)
        
        # Get response from chatbot service
        response = get_chat_response(
            query=request.query,
            category=request.category,
            language=request.language,
            retriever=retriever,
            llm=llm,
            memory=memory
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.post("/category/{category}", response_model=ChatResponse)
async def category_chat(
    category: str = Path(..., description="Legal category"),
    request: ChatRequest = None,
    retriever = Depends(get_retriever),
    llm = Depends(get_llm)
):
    """
    Process a category-specific chat request and return a response.
    
    - **category**: Legal category (from path)
    - **query**: User's question
    - **language**: Response language (default: English)
    - **session_id**: Unique session identifier
    - **messages**: Previous messages in the conversation (optional)
    """
    # Validate category
    if category not in settings.LEGAL_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {', '.join(settings.LEGAL_CATEGORIES)}")
    
    # If category is valid, update the request category field
    request.category = category
    
    try:
        # Get or create conversation memory for this session
        memory = get_conversation_memory(request.session_id)
        
        # Get response from chatbot service with strict category relevance check
        response = get_chat_response(
            query=request.query,
            category=category,
            language=request.language,
            retriever=retriever,
            llm=llm,
            memory=memory,
            strict_category_check=True  # Enforce strict category relevance
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@router.post("/session")
async def create_session():
    """Create a new chat session and return a session ID."""
    session_id = str(uuid4())
    return {"session_id": session_id}