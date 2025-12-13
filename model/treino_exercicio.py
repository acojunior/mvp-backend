from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from typing import Union

from  model import Treino, Exercicio, Base


class TreinoExercicio(Base):
    """
    Essa classe representa a associação entre o Treno e o Exercicío,
    adicionando a quantidade de repetições prescritas pelo instrutor.
    """
    __tablename__ = 'treino_exercicios'

    id_treino = Column(ForeignKey("treino.id"), primary_key=True)
    id_exercicio = Column(ForeignKey("exercicio.id"), primary_key=True)
    series = Column(Integer, nullable=False)
    repeticoes = Column(Integer, nullable=False)

    # relacionamento ORM.
    treino = relationship("Treino", back_populates="treino_exercicios")
    exercicio = relationship("Exercicio", back_populates="treino_exercicios")

    def __init__(self, treino, exercicio, series:int, repeticoes:int):
        """
        Cria o relacionamento entre o Treino e o Exercicio

        Arguments:
            treino: model do treino.
            exercicio: model do exercício
            series: Numero de séries prescritas do exercicio
            repeticoes: Numero de repetições prescritas do exercicio
        """
        self.treino = treino
        self.exercicio = exercicio
        self.series = series
        self.repeticoes = repeticoes
