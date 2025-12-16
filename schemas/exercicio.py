from pydantic import BaseModel
from typing import Optional, List
from model.exercicio import Exercicio


class ExercicioSchema(BaseModel):
    """ Define como um novo exercício a ser inserido deve ser representado
    """
    nome: str = "Agachamento"


class ExercicioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do exercício.
    """
    id: int = 1

class ExercicioUpdateSchema(BaseModel):
    """ Define como deve ser a estrutura para atualizar um exercício existente
    """
    id: int = 1
    nome: str = "Agachamento"


class ExercicioViewSchema(BaseModel):
    """ Define como um exercício será retornado.
    """
    id: int = 1
    nome: str = "Supino inclinado"


class ListagemExerciciosSchema(BaseModel):
    """ Define como uma listagem de exercícios será retornada.
    """
    exercicio:List[ExercicioViewSchema]


def apresenta_exercicios(exercicios: List[Exercicio]):
    """ Retorna uma representação do exercício seguindo o schema definido em
        ExercicioViewSchema.
    """
    result = []
    for exercicio in exercicios:
        result.append({
            "id": exercicio.id,
            "nome": exercicio.nome,
        })

    return {"exercicios": result}


class ExercicioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_exercicio(exercicio: Exercicio):
    """ Retorna uma representação do exercício seguindo o schema definido em
        ExercicioViewSchema.
    """
    return {
        "id": exercicio.id,
        "nome": exercicio.nome,
    }
