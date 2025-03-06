from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory

from app.services.translation import translate_text
from app.config import settings


def get_chat_response(
    query: str,
    category: str,
    language: str,
    retriever,
    llm,
    memory: ConversationBufferWindowMemory
):
    """
    Process a user query and return a response using RAG architecture.
    
    Args:
        query: User's question
        category: Legal category
        language: Response language
        retriever: Vector store retriever
        llm: Language model
        memory: Conversation memory
        
    Returns:
        Dictionary with answer and sources
    """
    # Add category context to the query
    enhanced_query = f"[Category: {category}] {query}"
    
    # Setup QA chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    
    # Get response
    result = qa({"question": enhanced_query})
    
    # Extract answer and sources
    english_response = result["answer"]
    source_documents = result.get("source_documents", [])
    
    # Extract source filenames
    sources = []
    for doc in source_documents:
        if hasattr(doc, "metadata") and "source" in doc.metadata:
            source = doc.metadata["source"]
            if source not in sources:
                sources.append(source)
    
    # Translate response if needed
    final_response = english_response
    if language != "English" and settings.ENABLE_TRANSLATION:
        final_response = translate_text(
            text=english_response, 
            source_lang="English", 
            target_lang=language,
            llm=llm
        )
    
    return {
        "answer": final_response,
        "sources": sources
    }