from config import *
from ingest_v2 import load_and_split_pdf_semantic, create_vector_store_v2, create_hybrid_retriever
from rag_chain_v2 import create_rag_chain_v2

pdf_path = "arquivos/NVIDIA.pdf"

print('\n[1/4] Semantic chunking do PDF: ')
docs = load_and_split_pdf_semantic(pdf_path)
print(f'{len(docs)} chunks.\n')

print('\n[2/4] VectorDB:')
vector_store = create_vector_store_v2(docs)
print('Pronto\n')

print('\n[3/4] Hybrid Retriever:')
hybrid_retriever = create_hybrid_retriever(vector_store, docs)
print('Pronto\n')

print('\n[4/4] Chain of thought:')
conversation = create_rag_chain_v2(hybrid_retriever)
print('Pronto\n')

session_id = "Pedro1"
print(f"\nSession id: {session_id}\n")

question1 = "Quais são os riscos específicos mencionados sobre a 'U.S. Government's October 2023 export controls'?"
print(f'\nPergunta: {question1}')
res = conversation.invoke(
    {"input": question1},
    config={"configurable": {'session_id': session_id}}
)
print(f'Resposta: {res['answer']}')

question2 = "Explique a relação entre a arquitetura Blackwell e as projeções de receita para o segmento de Data Center."
print(f'\nPergunta: {question2}')
res = conversation.invoke(
    {"input": question2},
    config={"configurable": {'session_id': session_id}}
)
print(f'Resposta: {res['answer']}')

question3 = "Qual foi o valor exato em dólares da 'inventory write-downs' no ano fiscal de 2024?"
print(f'\nPergunta: {question3}')
res = conversation.invoke(
    {"input": question3},
    config={"configurable": {'session_id': session_id}}
)
print(f'Resposta: {res['answer']}')