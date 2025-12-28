from pydantic import BaseModel, Field
from typing import List

class RelatorioExecutivo(BaseModel):
      veredito_final: str = Field(description="Decisão clara (Investir, Não Investir ou Cautela) e justificativa curta")
      percentual_score: float = Field(description="O percentual final (ex: 65.0)")
      detalhamento_notas: List[str] = Field(description="Lista de strings no formato 'Pilar (Nota X): Descrição'")
      sumario_executivo: str = Field(description="Resumo de alto nível")
      analise_mercado: str = Field(description="Insights sobre demanda e concorrência")
      viabilidade_financeira: str = Field(description="Análise de custos e ROI")
      matriz_riscos: List[str] = Field(description="Lista com os principais pontos de atenção e ameaças")
      conclusao_e_proximos_passos: List[str] = Field(description="Lista de ações recomendadas e conclusões práticas, separadas por itens.")