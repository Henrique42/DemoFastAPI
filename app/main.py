from fastapi import FastAPI  
from fastapi.middleware.cors import CORSMiddleware  
  
from app import models  
from app.database import engine  
from app.routers import cliente_routes, produto_routes

models.Base.metadata.create_all(bind=engine)  
  
app = FastAPI()  
  
origins = [  
    "http://localhost:8000",  
]  
  
app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  
  
  
app.include_router(cliente_routes.router, tags=["Cliente"], prefix="/api/v1/clientes")
app.include_router(produto_routes.router, tags=["Produto"], prefix="/api/v1/produtos")  

@app.get("/")  
def root():  
    return {"message": "Página inicial da API!!"}
  
@app.get("/api/healthchecker")  
def root():  
    return {"message": "API em funcionamento!!"}
