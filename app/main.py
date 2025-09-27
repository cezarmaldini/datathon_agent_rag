from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vaga_routers

app = FastAPI(
    title="Sistema de Gestão de Vagas",
    description="API para gerenciamento de vagas de emprego",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(vaga_routers.router)

@app.get("/")
async def root():
    return {"message": "Sistema de Gestão de Vagas API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}