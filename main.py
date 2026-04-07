from config import *
from ingest import load_and_split_pdf, create_vector_store
from rag_chain import create_rag_chain

pdf_path = "Atos-2024.pdf"

print("\nPDF fragmentado em:")
docs = load_and_split_pdf(pdf_path)
print(f"{len(docs)} chunks.\n")

print("\nVector DB:")
vector_store = create_vector_store(docs)
print("Funcionando\n")

print("\nRAG chain:")
qa_chain = create_rag_chain(vector_store)
print("Pronto\n")

question = 'Show me a recovery of the commercial activity in Q4 2024'
print(f"Pergunta: {question}")
res = qa_chain.invoke({"query": question})
print(f"Resposta: {res["result"]}")