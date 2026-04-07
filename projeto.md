Sistema RAG 
 
1. Fundamentação Teórica: Arquitetura RAG e Recuperação Semântica 
O Retrieval-Augmented Generation (RAG) é um framework arquitetural projetado para mitigar as limitações intrínsecas dos Large Language Models (LLMs), especificamente a alucinação (geração de informações factualmente incorretas) e o limite de corte de conhecimento. 
1.1. Representação Vetorial e Espaço Latente 
A base do RAG reside na Busca Semântica. Diferente da busca por palavras-chave (lexical), utilizamos modelos de Embeddings para converter texto em vetores de alta dimensão em um espaço latente. A proximidade semântica entre dois textos pode ser calculada através da Similaridade de Cosseno. 
1.2. Estratégias de Chunking e Context Window 
LLMs possuem um limite de tokens (Context Window). Inserir um PDF inteiro no prompt pode ser ineficiente e custoso. Portanto, aplicamos o Chunking: 
Fixed-size splitting: Divisão por número de caracteres/tokens. 
Recursive Character Splitting: Divisão inteligente que respeita parágrafos e pontuações para manter a semântica. 
Overlap: Uma porcentagem de repetição entre blocos (ex: 10%) para garantir que o contexto não seja cortado abruptamente entre dois chunks. 
Existem MUITAS estratégias de chunking e cada uma será mais adequada dependendo do cenário. 
1.3. O Fluxo de Inferência 
O processo segue o pipeline: 
Retrieval: O sistema busca os documentos com maior score de similaridade. 
Augmentation: Os documentos recuperados são injetados em um Prompt estruturado (ex: "Use apenas os trechos abaixo para responder..."). 
Generation: O modelo gera a resposta baseada exclusivamente nas evidências fornecidas. 
 
Objetivo do Projeto 
Este projeto consiste na criação de um sistema de consulta a documentos PDF utilizando a arquitetura RAG. A aplicação deve oferecer uma funcionalidade de upload de PDFs que, por meio de um pipeline de processamento, extrai o texto e realiza a indexação semântica em um banco de vetores local (ChromaDB ou FAISS). Chatbot conectado à Azure OpenAI atuará como interface de consulta, consumindo os vetores previamente indexados para fundamentar suas respostas nos documentos fornecidos pelo usuário. 
A Figura abaixo é um exemplo do fluxo RAG. 
  
Requisitos Técnicos e Ferramentas 
Linguagem: Python 3.10+, Flask/FastAPI 
LLM: Azure OpenAI (GPT-4o mini ou similar). 
Embeddings: Azure OpenAI (text-embedding-3-small ou similar). 
Orquestração: LangChain 
Interface: Streamlit ou React 
Docker 
 
Passo a Passo simplificado do desenvolvimento 
Fase 1: Preparação do Ambiente 
Configure um recurso da Azure OpenAI no portal Azure e faça o deploy dos modelos de Chat e Embedding. 
Prepare o arquivo .env para armazenar chaves de API e endpoints (nunca suba chaves no Git!). 
Fase 2: Ingestão de Documentos 
Implementar um script que carregue arquivos PDF. Utilizem Relatórios Anuais ESG e formulários de referência de empresas. 
Realizar o Text Splitting: Divida o texto em partes. Pesquise estratégias e escolha a que você consedera mais promissora. 
Criar um Vector Store temporário (pode usar o FAISS ou Chroma) para armazenar os embeddings desses pedaços. 
Fase 3: O Motor RAG (Chain) 
Configurar a conexão com o modelo de chat da Azure. 
Criar uma função que: 
Recebe a pergunta do usuário. 
Busca os contextos relevantes no Vector Store. 
Envia o prompt formatado para a IA. 
Fase 4: Persistência e Memória 
Usar a memória do Langchain para a manuteção de histórico de conversas. 
Fase 5: Interface e Deploy 
Desenvolver uma UI simples em Streamlit ou React. 
Rodar a aplicação em Docker na máquina local. 
 
Critérios de Entrega 
Cada Sprint terá a duração de 3 semanas, de forma a acomodar as demandas em paralelo. 
Sprint 1 – Setup do sistema 
A aplicação deve permitir o upload de documentos pdf e informar o usuário sobre o envio para processamento. 
A aplicação deve fornecer respostas baseadas exclusivamente nos documentos enviados. 
A aplicação deve rodar em docker. 
O código deve estar versionado no GitHub com um README.md explicativo. 
 
Sprint 2 – Refinamento e avaliação 
Você deve construir um dataset ‘ouro’ com no mínimo 30 perguntas e respostas para avaliar o desempenho do chatbot. Este dataset deve conter exemplos de perguntas que não estão nos documentos de teste. 
Você deve desenvolver um script que utiliza um LLM para comparar as respostas do seu chatbot com o padrão ‘ouro’ e atribuir um score de avaliação. 