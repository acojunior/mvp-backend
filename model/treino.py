from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Treino(Base):
    __tablename__ = 'treino'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o treino e exercicio.
    # A relação é representada na tabela treino_exercicios.
    treino_exercicios = relationship(
        "TreinoExercicio",
        back_populates="treino",
        # Deleta em cascata, ou seja, caso seja deletado um treino
        # as tuplas de relacionamento do mesmo serão deletadas.
        cascade="all, delete-orphan",
    )

    # Definição do relacionamento entre o cliente e treino.
    # A relação é representada na tabela cliente_treinos.
    cliente_treinos = relationship(
        "ClienteTreino",
        back_populates="treino",
        # Deleta em cascata, ou seja, caso seja deletado um treino
        # as tuplas de relacionamento do mesmo serão deletadas.
        cascade="all, delete-orphan"
    )

    def __init__(self, nome:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Treino

        Arguments:
            nome: nome do treino.
            data_insercao: data de quando o treino foi inserido à base
        """
        self.nome = nome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
