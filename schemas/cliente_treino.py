from pydantic import BaseModel


class TreinoDoClienteSchema(BaseModel):
    """ Representa o treino de um cliente
    """
    id_treino: int = 1
    dia_semana: str = "TERCA"
