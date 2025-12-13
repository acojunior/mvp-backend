from pydantic import BaseModel


class ExercicioNoTreinoSchema(BaseModel):
    """ Representa um exercício dentro de um treino
    """
    id_exercicio: int = 1
    series: int = 4
    repeticoes: int = 12
