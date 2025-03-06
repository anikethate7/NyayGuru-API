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
    memory: ConversationBufferWindowMemory,
    strict_category_check: bool = False
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
        strict_category_check: Whether to enforce strict category relevance
        
    Returns:
        Dictionary with answer and sources
    """
    # Add category context to the query
    enhanced_query = f"[Category: {category}] {query}"
    
    # If strict category check is enabled, first verify query relevance
    if strict_category_check:
        relevance_check = check_category_relevance(query, category, llm)
        if not relevance_check["is_relevant"]:
            return {
                "answer": relevance_check["message"],
                "sources": []
            }
    
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


def check_category_relevance(query: str, category: str, llm):
    """
    Check if a query is relevant to the specified legal category.
    
    Args:
        query: User's question
        category: Legal category
        llm: Language model
        
    Returns:
        Dictionary with relevance check result
    """
    prompt = f"""
    You are a legal expert responsible for routing questions to the appropriate department.
    
    Task:
    Determine if the following question is directly related to the legal category: "{category}".
    
    Question: "{query}"
    
    Guidelines:
    - Only respond with "YES" if the question is clearly and directly related to {category}.
    - Otherwise respond with "NO".
    - Do not provide any explanation or additional context.
    - Respond with only a single word: "YES" or "NO".
    """
    
    response = llm.invoke(prompt)
    is_relevant = response.content.strip().upper() == "YES"
    
    if is_relevant:
        return {
            "is_relevant": True,
            "message": ""
        }
    else:
        return {
            "is_relevant": False,
            "message": f"I'm sorry, but your question doesn't appear to be related to the '{category}' category. Please ask a question specifically about {category} or select a different legal category."
        }