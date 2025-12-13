from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Exercicio(Base):
    __tablename__ = 'exercicio'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o treino e exercicio.
    # A relação é representada na tabela treino_exercicios.
    treino_exercicios = relationship(
        "TreinoExercicio",
        back_populates="exercicio",
        # Deleta em cascata, ou seja, caso seja deletado um treino
        # as tuplas de relacionamento do mesmo serão deletadas.
        cascade="all, delete-orphan",
    )

    def __init__(self, nome:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Exercicio

        Arguments:
            nome: nome do exercício.
            data_insercao: data de quando o exercicio foi feito ou inserido
                           à base
        """
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao
