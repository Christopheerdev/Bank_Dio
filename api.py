from fastapi import FastAPI
from pydantic import BaseModel
from banco_ch import *

app = FastAPI()



class Users(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    endereco: str

class Conta(BaseModel):
    cpf: str


@app.post("/Criar_Conta/")
def criar_conta(conta: Conta):
    usuario = filtrar_usuario(conta.cpf)
    if not usuario:
        return {"message": "Usuário não encontrado!"}
    
    numero_conta = len(contas)+1
    nova_conta = ContaCorrente(
        numero_conta, usuario
    )
    usuario.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    return {"message": "Conta criada com sucesso!"}


@app.post("/Criar_Usuario/")
def criar_usuario(usuario: Users):
    if filtrar_usuario(usuario.cpf):
        return {"message": "Usuário já existe!"}
    
    novo_usuario = PessoaFisica(
        usuario.nome,
        usuario.cpf,
        usuario.data_nascimento,
        usuario.endereco
    )

    print("antes", usuarios)

    usuarios.append(novo_usuario)
    print("depois", usuarios)
    return {"message": "Usuário criado com sucesso!"}
    

@app.get("/Users/")
def listar_users():

    return {
        "usuarios": [
            {
                "nome": usuario.nome,
                "cpf": usuario.cpf,
                "data_nascimento": usuario.data_nascimento,
                "endereco": usuario.endereco
            }
            for usuario in usuarios
        ]
    }



#uvicorn api:app --reload