from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import *
from ingest import load_and_split_pdf, create_vector_store
from ingest_v2 import load_and_split_pdf_semantic, create_vector_store_v2, create_hybrid_retriever
from rag_chain import create_rag_chain
from rag_chain_v2 import create_rag_chain_v2
import shutil
import os
import uuid



# Configuração do FastAPI



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    question: str



# Primeiro endpoint: Upload de PDF



@app.post('/upload')
async def upload_pdf(
    file: UploadFile = File(...),
    strategy: str = Form(default='v1')
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas PDF")
    
    if strategy not in ('v1', 'v2'):
        raise HTTPException(status_code=400, detail='Strategy deve ser v1 ou v2')
    
    session_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_FOLDER, f"{session_id}.pdf")
    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)

    try:
        if strategy == 'v1':
            docs = load_and_split_pdf(file_path)
            vector_store = create_vector_store(docs)
            conversation = create_rag_chain(vector_store)

        else:
            docs = load_and_split_pdf_semantic(file_path)
            vector_store = create_vector_store_v2(docs)
            hybrid_retriever = create_hybrid_retriever(vector_store, docs)
            conversation = create_rag_chain_v2(hybrid_retriever)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'erro ao processar PDF: {str(e)}')
    
    sessions[session_id] = {
        'conversation': conversation,
        'strategy': strategy,
        'filename': file.filename,
        'chunks': len(docs)
    }

    return {
        'session_id': session_id,
        'strategy': strategy,
        'filename': file.filename,
        'chunks': len(docs),
        'message': f'Funcionando. Estrategia: {strategy}'
    }



#Segundo endpoint: Chat



@app.post('/chat')
async def chat(request: ChatRequest):
    session_id = request.session_id
    question = request.question

    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail='Sessão não encontrada. Upload do PDF primeiro.'
        )
    
    conversation = sessions[session_id]['conversation']

    try:
        result = conversation.invoke(
            {'input': question},
            config = {'configurable': {'session_id': session_id}}
        )
        answer = result['answer']
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao gerar resposta: {str(e)}')
    
    return {
        'answer': answer,
        'session_id': session_id,
        'strategy': sessions[session_id]['strategy']
    }