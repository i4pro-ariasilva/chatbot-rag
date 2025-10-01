@echo off
echo 🚀 Iniciando Chatbot RAG Otimizado...
echo.
echo 📊 Verificando dependências...
python -c "import fastapi, uvicorn, requests" 2>nul
if errorlevel 1 (
    echo ❌ Dependências não encontradas. Instalando...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erro na instalação. Verifique o Python e pip.
        pause
        exit /b 1
    )
)

echo ✅ Dependências OK
echo.
echo 🌐 Iniciando servidor em http://localhost:8000
echo 💡 Pressione Ctrl+C para parar o servidor
echo.

python backend/main.py

echo.
echo 🔴 Servidor finalizado.
pause