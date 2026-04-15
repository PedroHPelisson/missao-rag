from config import *
from ingest import load_and_split_pdf, create_vector_store
from rag_chain import create_rag_chain

pdf_path = "arquivos/NVIDIA.pdf"

print("\n[1/3] PDF fragmentado em:")
docs = load_and_split_pdf(pdf_path)
print(f"{len(docs)} chunks.\n")

print("\n[2/3] Vector DB:")
vector_store = create_vector_store(docs)
print("Funcionando\n")

print("\n[3/3] RAG chain:")
conversation = create_rag_chain(vector_store)
print("Pronto\n")

session_id = "Pedro1"
print(f'\nSession id: {session_id}\n')

print('\n\n')

question1 = "Quais são os riscos específicos mencionados sobre a 'U.S. Government's October 2023 export controls'?"
print(f"Pergunta: {question1}")
res = conversation.invoke(
    {'input': question1},
    config = {'configurable':{"session_id": session_id}}
)
print(f"Resposta: {res['answer']}\n\n")

question2 = "Explique a relação entre a arquitetura Blackwell e as projeções de receita para o segmento de Data Center."
print(f"Pergunta: {question2}")
res = conversation.invoke(
    {'input': question2},
    config = {'configurable':{"session_id": session_id}}
)
print(f"Resposta: {res['answer']}\n\n")

question3 = "Qual foi o valor exato em dólares da 'inventory write-downs' no ano fiscal de 2024?"
print(f"Pergunta: {question3}")
res = conversation.invoke(
    {'input': question3},
    config = {'configurable':{"session_id": session_id}}
)
print(f"Resposta: {res['answer']}\n\n")