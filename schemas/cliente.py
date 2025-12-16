from datetime import date
from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente

from schemas import TreinoDoClienteSchema


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    nome: str = "Antonio Carlos"
    data_nascimento: date = "1994-08-03"
    altura: float = 2.03
    peso: float = 110
    treinos: List[TreinoDoClienteSchema] = []


class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no id do cliente.
    """
    id: int = 1


class ClienteUpdateSchema(BaseModel):
    """ Define como deve ser a estrutura para atualizar um exercício existente
    """
    id: int = 1
    nome: str = "Antonio Carlos"
    data_nascimento: date = "1994-08-03"
    altura: float = 2.03
    peso: float = 110
    treinos: List[TreinoDoClienteSchema] = []


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado.
    """
    id: int = 1
    nome: str = "Antonio Carlos"
    data_nascimento: date = "1994-08-03"
    altura: float = 2.03
    peso: float = 100
    treinos: List[TreinoDoClienteSchema]


class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteViewSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:

        # Criando uma lista nova a partir do cliente_treinos
        # id_treino não é representado no ExercicioNoTreinoSchema
        lista_treinos = []
        for cliente_treino in cliente.cliente_treinos:
            lista_treinos.append({
                "id_treino": cliente_treino.treino.id,
                "dia_semana": cliente_treino.dia_semana,
            })

        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "data_nascimento": (
                cliente.data_nascimento.isoformat() 
                if cliente.data_nascimento else None
            ),
            "altura": cliente.altura,
            "peso": cliente.peso,
            "treinos": lista_treinos,
        })

    return {"clientes": result}


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """

    # Criando uma lista nova a partir do cliente_treinos
    # id_cliente não é representado no TreinoDoClienteSchema
    treinos = []
    for cliente_treino in cliente.cliente_treinos:
        treinos.append({
            "id_treino": cliente_treino.treino.id,
            "dia_semana": cliente_treino.dia_semana,
        })
    
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "data_nascimento": (
            cliente.data_nascimento.isoformat() 
            if cliente.data_nascimento else None
        ),
        "altura": cliente.altura,
        "peso": cliente.peso,
        "treinos": treinos,
    }
