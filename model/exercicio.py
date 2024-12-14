from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Descricao


class Exercicio(Base):
    __tablename__ = 'exercicio'

    id = Column("pk_exercicio", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    series = Column(Integer)  
    repeticoes = Column(Integer)
    quilos = Column(Float)

    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o exercicio e o descricao.
    # Essa relação é implicita, não está salva na tabela 'exercicio',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    descricoes = relationship("Descricao")

    def __init__(self, nome:str, series:int, repeticoes:int, quilos:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Exercicio

        Arguments:
            nome: nome do exercicio.
            series: quantidade de series do exercicio
            repeticoes: quantidade de repeticoes do exercicio
            quilos: quantos quilos para o exercicio
            data_insercao: data de quando o exercicio foi inserido à base
        """
        self.nome = nome
        self.series = series
        self.repeticoes = repeticoes
        self.quilos = quilos

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_descricao(self, descricao:Descricao):
        """ Adiciona uma nova descricao ao exercicio
        """
        self.descricoes.append(descricao)