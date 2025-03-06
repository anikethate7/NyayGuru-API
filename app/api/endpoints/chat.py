from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chatbot import get_chat_response
from app.dependencies import get_retriever, get_llm, get_conversation_memory

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


@router.post("/session")
async def create_session():
    """Create a new chat session and return a session ID."""
    session_id = str(uuid4())
    return {"session_id": session_id}