# Importa o modelo de Cliente
from app.models import Clientes

class ClientesController():
    # Inicializa o controlador com a sessão de banco
    def __init__(self, db_session):
        self.db = db_session

    # Método para adicionar um novo cliente
    def add_cliente(self, cliente_info):
        new_cliente = Clientes(**cliente_info)  # Cria um novo cliente com os dados fornecidos
        try:
            self.db.add(new_cliente)  # Adiciona o cliente à sessão
            self.db.commit()          # Confirma a transação
            self.db.refresh(new_cliente)  # Atualiza os dados do cliente
        except Exception as e:
            self.db.rollback()  # Desfaz a transação em caso de erro
            return {"success": False, "message": "Erro ao adicionar cliente", "payload": None}
        return {"success": True, "message": "Cliente adicionado com sucesso", "payload": {
            "id": new_cliente.id,
            "nome": new_cliente.nome,
            "email": new_cliente.email,
            "cpf": new_cliente.cpf
        }}

    # Método para obter todos os clientes
    def get_all_clientes(self):
        all_clientes = self.db.query(Clientes).all()  # Consulta todos os clientes
        resp = []
        for cliente in all_clientes:
            resp.append({
                "id": cliente.id,
                "nome": cliente.nome,
                "email": cliente.email,
                "cpf": cliente.cpf,
                "ativo": cliente.ativo
            })
        return {"success": True, "message": "Clientes retornados com sucesso", "payload": resp}
