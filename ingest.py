from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS,
    CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_STORE_PATH
)

def load_and_split_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP 
    )
    return text_splitter.split_documents(documents)


def create_vector_store(documents): 
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint = AZURE_OPENAI_ENDPOINT,
        api_key = AZURE_OPENAI_API_KEY,
        deployment = AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDINGS
    )

    #print('\nChaves OK\n')

    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embeddings,
        persist_directory = VECTOR_STORE_PATH
    )

    #vector_store.persist(): Pelo que entendi, já roda automaticamente nas versões recentes.
    return vector_store

#pdf_path = "Atos-2024.pdf"
#docs = load_and_split_pdf(pdf_path)
#vector_store = create_vector_store(docs)
#print(f"\nVectorDB OK. {len(docs)} chunks.\n")