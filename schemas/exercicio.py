from pydantic import BaseModel
from typing import Optional, List
from model.exercicio import Exercicio

from schemas import DescricaoSchema


class ExercicioSchema(BaseModel):
    """ Define como um novo exercicio a ser inserido deve ser representado
    """
    nome: str = "Supino com Halteres"
    series: Optional[int] = 3
    repeticoes: Optional[int] = 10
    quilos: Optional [float] = 25.5


class ExercicioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do exercicio.
    """
    nome: str = "Teste"


class ListagemExerciciosSchema(BaseModel):
    """ Define como uma listagem de exercicios será retornada.
    """
    exercicios:List[ExercicioSchema]


def apresenta_exercicios(exercicios: List[Exercicio]):
    """ Retorna uma representação do exercicio seguindo o schema definido em
        ExercicioViewSchema.
    """
    result = []
    for exercicio in exercicios:
        result.append({
            "nome": exercicio.nome,
            "series": exercicio.series,
            "repeticoes": exercicio.repeticoes,
            "quilos": exercicio.quilos,
        })

    return {"exercicios": result}


class ExercicioViewSchema(BaseModel):
    """ Define como um exercicio será retornado: exercicio + descricoes.
    """
    id: int = 1
    nome: str = "Supino com Halteres"
    series: Optional[int] = 3
    repeticoes: int = 10
    quilos: float = 25.5
    descricao:List[DescricaoSchema]


class ExercicioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_exercicio(exercicio: Exercicio):
    """ Retorna uma representação do exercicio seguindo o schema definido em
        ExercicioViewSchema.
    """
    return {
        "id": exercicio.id,
        "nome": exercicio.nome,
        "series": exercicio.series,
        "repeticoes": exercicio.repeticoes,
        "total_descricoes": len(exercicio.descricoes),
        "descricoes": [{"texto": c.texto} for c in exercicio.descricoes]
    }
