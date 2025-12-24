from typing import Annotated, List, TypedDict, Dict
import operator

class AgentState(TypedDict):
      problema: str
      plano: List[str]
      querys_de_pesquisa: List[str]
      conteudo_pesquisado: Annotated[List[Dict], operator.add] 
      numero_iteracao: Annotated[int, operator.add]
      feedback_critico: str
      aprovado: bool
      notas_viabilidade: Dict[str, Dict]
      percentual_final: float
      relatorio_final: str


      