from typing import Annotated, List, TypedDict, Dict, Union
from project.utils.schema_refinador import RelatorioExecutivo
import operator

class AgentState(TypedDict):
      problema: str
      plano: List[str]
      querys_de_pesquisa: List[str]
      conteudo_pesquisado: Annotated[List[Dict], operator.add] 
      iteracao_pesquisa: Annotated[int, operator.add]
      iteracao_critica: Annotated[int, operator.add]
      feedback_critico: str
      instrucoes_refinamento: str
      proximo_passo: str
      aprovado: bool
      notas_viabilidade: Dict[str, Dict]
      percentual_final: float
      relatorio_final: Union[str, RelatorioExecutivo]


      