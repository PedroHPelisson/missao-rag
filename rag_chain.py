from langchain_openai import AzureChatOpenAI
from langchain_classic.chains import RetrievalQA
from config import (
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME_CHAT
)

def create_rag_chain(vector_store):
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME_CHAT,
        api_version="2023-12-01-preview",
        temperature=0
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    return qa_chain

#TESTE
#from ingest import load_and_split_pdf, create_vector_store
#pdf_path = "Atos-2024.pdf"
#docs = load_and_split_pdf(pdf_path)
#vector_store = create_vector_store(docs)
#qa_chain = create_rag_chain(vector_store)

#question = 'Show me a recovery of the commercial activity in Q4 2024'
#response = qa_chain.invoke(question)

#print(f"\nPergunta: {question}\n")
#print(f"\nResposta: {response}\n")