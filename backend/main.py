#!/usr/bin/env python3
"""
Servidor FastAPI super otimizado para Chatbot RAG
Versão 3.0 com máxima performance
"""
import sys
import os
import logging
import time
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Adiciona paths necessários
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = current_dir
project_dir = os.path.dirname(current_dir)

sys.path.extend([project_dir, backend_dir])

# Imports otimizados
from backend.document_processor import DocumentProcessor
from backend.rag_engine import FastSimpleRAGEngine
from config.settings import config

# Configure logging otimizado
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with optimizations
app = FastAPI(
    title="Chatbot RAG Ultra Otimizado",
    description="AI-powered chatbot with maximum performance optimizations",
    version="3.0.0"
)

# Configure CORS otimizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Mount static files
frontend_path = os.path.join(project_dir, "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Global components
document_processor = None
rag_engine = None
is_initialized = False
initialization_time = 0
performance_metrics = {
    "total_queries": 0,
    "average_response_time": 0,
    "cache_hits": 0,
    "api_calls": 0
}

# Pydantic models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    processing_time: Optional[float] = None

class SystemStatus(BaseModel):
    status: str
    documents_indexed: int
    collection_info: Dict[str, Any]
    performance_metrics: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system with optimization."""
    global document_processor, rag_engine, is_initialized, initialization_time
    
    start_time = time.time()
    
    try:
        logger.info("🚀 Starting ULTRA-OPTIMIZED RAG system...")
        
        logger.info("📄 Initializing optimized document processor...")
        document_processor = DocumentProcessor()
        
        logger.info("🧠 Initializing ultra-fast RAG engine...")
        rag_engine = FastSimpleRAGEngine()
        
        # Check documents directory
        if not os.path.exists(config.DOCUMENTS_DIR):
            logger.warning(f"Documents directory not found: {config.DOCUMENTS_DIR}")
            is_initialized = True
            initialization_time = time.time() - start_time
            return
        
        # Process and index documents
        logger.info("📚 Processing documents with optimization...")
        documents = document_processor.process_all_documents()
        
        if documents:
            logger.info(f"📊 Indexing {len(documents)} documents...")
            success = rag_engine.index_documents(documents)
            
            if success:
                initialization_time = time.time() - start_time
                logger.info(f"✅ System initialized in {initialization_time:.2f}s!")
                is_initialized = True
            else:
                logger.error("❌ Failed to index documents")
        else:
            logger.warning("⚠️ No documents found")
            is_initialized = True
            initialization_time = time.time() - start_time
            
    except Exception as e:
        logger.error(f"❌ Error during initialization: {e}")
        initialization_time = time.time() - start_time

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Serve the chat interface."""
    try:
        frontend_file = os.path.join(frontend_path, "index.html")
        if os.path.exists(frontend_file):
            with open(frontend_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return HTMLResponse(content=content)
        else:
            return HTMLResponse("""
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🚀 Ultra-Optimized RAG Chatbot</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        max-width: 800px; 
                        margin: 0 auto; 
                        padding: 20px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        min-height: 100vh;
                    }
                    .container {
                        background: rgba(255,255,255,0.1);
                        padding: 20px;
                        border-radius: 15px;
                        backdrop-filter: blur(10px);
                    }
                    #chat-container { margin-top: 20px; }
                    #messages { 
                        height: 400px; 
                        overflow-y: auto; 
                        border: 1px solid rgba(255,255,255,0.3); 
                        padding: 15px; 
                        margin-bottom: 15px; 
                        border-radius: 10px;
                        background: rgba(0,0,0,0.2);
                    }
                    #query-input { 
                        width: 70%; 
                        padding: 12px; 
                        border: none;
                        border-radius: 25px;
                        font-size: 16px;
                    }
                    button { 
                        padding: 12px 25px; 
                        background: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 25px;
                        margin-left: 10px;
                        cursor: pointer;
                        font-size: 16px;
                    }
                    button:hover { background: #45a049; }
                    .message { margin: 10px 0; padding: 10px; border-radius: 10px; }
                    .user { background: rgba(76, 175, 80, 0.3); text-align: right; }
                    .bot { background: rgba(33, 150, 243, 0.3); }
                    .performance { font-size: 12px; color: #ccc; }
                    h1 { text-align: center; margin-bottom: 30px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Ultra-Optimized RAG Chatbot</h1>
                    <div id="status">Verificando status do sistema...</div>
                    <div id="chat-container">
                        <div id="messages"></div>
                        <input type="text" id="query-input" placeholder="Digite sua pergunta..." disabled>
                        <button onclick="sendQuery()" disabled id="send-btn">Enviar</button>
                        <button onclick="clearCache()" style="background: #ff9800;">Limpar Cache</button>
                    </div>
                </div>
                
                <script>
                    let systemReady = false;
                    
                    async function checkStatus() {
                        try {
                            const response = await fetch('/status');
                            const data = await response.json();
                            const statusDiv = document.getElementById('status');
                            
                            if (data.status === 'ready') {
                                statusDiv.innerHTML = `✅ Sistema pronto! ${data.documents_indexed} documentos indexados`;
                                systemReady = true;
                                document.getElementById('query-input').disabled = false;
                                document.getElementById('send-btn').disabled = false;
                            } else {
                                statusDiv.innerHTML = `⏳ ${data.status}... Aguarde`;
                                setTimeout(checkStatus, 2000);
                            }
                        } catch (error) {
                            document.getElementById('status').innerHTML = '❌ Erro na conexão';
                            setTimeout(checkStatus, 5000);
                        }
                    }
                    
                    async function sendQuery() {
                        if (!systemReady) return;
                        
                        const queryInput = document.getElementById('query-input');
                        const query = queryInput.value.trim();
                        if (!query) return;
                        
                        const messagesDiv = document.getElementById('messages');
                        const startTime = Date.now();
                        
                        messagesDiv.innerHTML += 
                            `<div class="message user"><strong>Você:</strong> ${query}</div>`;
                        
                        queryInput.value = '';
                        queryInput.disabled = true;
                        document.getElementById('send-btn').disabled = true;
                        
                        try {
                            const response = await fetch('/chat', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({query: query})
                            });
                            
                            const data = await response.json();
                            const responseTime = Date.now() - startTime;
                            
                            messagesDiv.innerHTML += 
                                `<div class="message bot">
                                    <strong>🤖 Assistente:</strong> ${data.response}
                                    <div class="performance">⚡ ${responseTime}ms | Fontes: ${data.sources.length}</div>
                                </div>`;
                            
                            messagesDiv.scrollTop = messagesDiv.scrollHeight;
                            
                        } catch (error) {
                            messagesDiv.innerHTML += 
                                `<div class="message bot">❌ Erro: ${error.message}</div>`;
                        } finally {
                            queryInput.disabled = false;
                            document.getElementById('send-btn').disabled = false;
                            queryInput.focus();
                        }
                    }
                    
                    async function clearCache() {
                        try {
                            const response = await fetch('/clear-cache', { method: 'POST' });
                            const data = await response.json();
                            alert(data.message);
                        } catch (error) {
                            alert('Erro ao limpar cache');
                        }
                    }
                    
                    document.getElementById('query-input').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            sendQuery();
                        }
                    });
                    
                    checkStatus();
                </script>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving chat interface: {e}")
        return HTMLResponse("<h1>Error loading chat interface</h1>")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Ultra-optimized chat endpoint."""
    if not is_initialized:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG engine not available")
    
    start_time = time.time()
    
    try:
        global performance_metrics
        performance_metrics["total_queries"] += 1
        
        logger.info(f"🔍 Processing query: {request.query[:50]}...")
        
        result = rag_engine.chat(request.query)
        processing_time = time.time() - start_time
        
        # Update metrics
        total_time = performance_metrics["average_response_time"] * (performance_metrics["total_queries"] - 1)
        performance_metrics["average_response_time"] = (total_time + processing_time) / performance_metrics["total_queries"]
        
        logger.info(f"⚡ Query processed in {processing_time:.3f}s")
        
        return ChatResponse(
            response=result.get('response', 'No response generated'),
            sources=result.get('sources', []),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get system status."""
    try:
        if not is_initialized:
            return SystemStatus(
                status="initializing",
                documents_indexed=0,
                collection_info={},
                performance_metrics=performance_metrics
            )
        
        collection_info = {}
        documents_count = 0
        
        if rag_engine:
            collection_info = rag_engine.get_collection_info()
            documents_count = collection_info.get('document_count', 0)
        
        return SystemStatus(
            status="ready" if is_initialized else "initializing",
            documents_indexed=documents_count,
            collection_info=collection_info,
            performance_metrics=performance_metrics
        )
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail="Error getting system status")

@app.post("/clear-cache")
async def clear_cache():
    """Clear all caches."""
    try:
        if rag_engine:
            rag_engine.clear_cache()
            logger.info("🧹 All caches cleared")
            return {"message": "Caches cleared successfully", "status": "success"}
        else:
            return {"message": "RAG engine not initialized", "status": "warning"}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail="Error clearing cache")

@app.get("/health")
async def health_check():
    """Fast health check."""
    return {
        "status": "healthy" if is_initialized else "initializing",
        "timestamp": time.time(),
        "version": "3.0.0-ultra-optimized"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Ultra-Optimized Chatbot RAG Server...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )