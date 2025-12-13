from pydantic import BaseModel
from typing import Optional, List
from model.treino import Treino

from schemas import ExercicioNoTreinoSchema


class TreinoSchema(BaseModel):
    """ Define como um novo treino a ser inserido deve ser representado
    """
    nome: str = "Treino de Peito"
    exercicios: List[ExercicioNoTreinoSchema] = []


class TreinoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no id do treino.
    """
    id: int = 1


class TreinoUpdateSchema(BaseModel):
    """ Define como deve ser a estrutura para atualizar um exercício existente
    """
    id: int = 1
    nome: str = "Agachamento"
    exercicios: List[ExercicioNoTreinoSchema] = []


class ListagemTreinosSchema(BaseModel):
    """ Define como uma listagem de treinos será retornada.
    """
    treinos:List[TreinoViewSchema]


def apresenta_treinos(treinos: List[Treino]):
    """ Retorna uma representação do treino seguindo o schema definido em
        TreinoViewSchema.
    """
    result = []
    for treino in treinos:

        # Criando uma lista nova a partir do treino_exercicios
        # id_treino não é representado no ExercicioNoTreinoSchema
        exercicios = []
        for treino_exercicio in treino.treino_exercicios:
            exercicios.append({
                "id_exercicio": treino_exercicio.exercicio.id,
                "series": treino_exercicio.series,
                "repeticoes": treino_exercicio.repeticoes,
            })
            
        result.append({
            "id": treino.id,
            "nome": treino.nome,
            "exercicios": exercicios,
        })

    return {"treinos": result}


class TreinoViewSchema(BaseModel):
    """ Define como um treino será retornado.
    """
    id: int = 1
    nome: str = "Treino de Peito"
    exercicios: List[ExercicioNoTreinoSchema]


class TreinoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_treino(treino: Treino):
    """ Retorna uma representação do treino seguindo o schema definido em
        TreinoViewSchema.
    """

    # Criando uma lista nova a partir do treino_exercicios
    # id_treino não é representado no ExercicioNoTreinoSchema
    exercicios = []
    for te in treino.treino_exercicios:
        exercicios.append({
            "id_exercicio": te.exercicio.id,
            "series": te.series,
            "repeticoes": te.repeticoes,
        })
    
    return {
        "id": treino.id,
        "nome": treino.nome,
        "exercicios": exercicios,
    }
