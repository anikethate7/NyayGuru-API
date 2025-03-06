import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import settings

def embed_and_save_documents(data_dir="./LEGAL-DATA"):
    """
    Load PDF documents, split them into chunks, embed them, and save to disk.
    
    Args:
        data_dir: Directory containing PDF files
    """
    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL)
    
    # Load documents
    loader = PyPDFDirectoryLoader(data_dir)
    print("Loader initialized")
    docs = loader.load()
    print(f"Loaded {len(docs)} documents")
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE, 
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    final_documents = text_splitter.split_documents(docs)
    print(f"Split into {len(final_documents)} chunks")
    
    # Ensure metadata includes the source file name
    for doc in final_documents:
        if 'source' in doc.metadata:
            source_file = doc.metadata['source']
            doc.metadata['source'] = os.path.basename(source_file)
        else:
            # If source metadata is not present, add it
            doc.metadata['source'] = os.path.basename(data_dir)
    
    # Batch documents to avoid payload size limits
    batch_size = 100
    batched_documents = [
        final_documents[i:i + batch_size] 
        for i in range(0, len(final_documents), batch_size)
    ]
    
    # Create vector stores for each batch
    print(f"Processing {len(batched_documents)} batches")
    vector_stores = []
    for i, batch in enumerate(batched_documents):
        print(f"Processing batch {i+1}/{len(batched_documents)}")
        vector_store = FAISS.from_documents(batch, embeddings)
        vector_stores.append(vector_store)
    
    # Merge vector stores
    vectors = vector_stores[0]
    for vector_store in vector_stores[1:]:
        vectors.merge_from(vector_store)
    print("Merged vector stores")
    
    # Save to disk
    vectors.save_local(settings.VECTOR_STORE_PATH)
    print(f"Saved vector store to {settings.VECTOR_STORE_PATH}")
    
    return len(final_documents)