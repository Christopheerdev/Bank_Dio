from fastapi import FastAPI
from pydantic import BaseModel
from banco_ch import *

app = FastAPI()



class Conta(BaseModel):
    nome: str
    data_nascimento: str
    endereco: str
    cpf: str
    agencia: str
    numero_conta: int
    limite: float


@app.post("/Criar_Conta/")
def criar_conta(conta: Conta):
        conta_nova ={
        "nome": conta.nome,
        "cpf": conta.cpf,
        "data_nascimento": conta.data_nascimento,
        "endereco": conta.endereco,
        "agencia": conta.agencia,
        "numero_conta": conta.numero_conta, 
        "limite": conta.limite,
        }
        contas.append(conta_nova)
        
        return {"message": "Conta criada com sucesso!"}
    
     

@app.get("/Contas/")
def listar_contas():
    return contas

@app.get("/Selecionar_Conta/")
def get_account(agencia: str,):
    for conta in contas:
        if conta["agencia"] == agencia:
            return conta
    return {"message": "Conta não encontrada."}


@app.post("/Depositar/")
def depositar(agencia: str, valor: float):
    for conta in contas:
        if conta["agencia"] == agencia:
            conta["limite"] += valor
            return {"message": f"Depósito realizado com sucesso para {conta['nome']}!", "novo_limite": conta["limite"]}
    return {"message": "Conta não encontrada."}


@app.post("/Sacar/")
def sacar(agencia: str, valor: float):
    for conta in contas:
        if conta["agencia"] == agencia:
            if valor > conta["limite"]:
                return {"message": "Saldo insuficiente!"}
            conta["limite"] -= valor
            return {"message": f"Saque realizado com sucesso para {conta['nome']}!", "novo_limite": conta["limite"]}
        
    return {"message": "Conta não encontrada."}

@app.get("/Historico/")
def historico(agencia: str):
    for conta in contas:
        if conta["agencia"] == agencia:
            return {"message": f"Histórico de transações para {conta['nome']}!"}
    return {"message": "Conta não encontrada."}