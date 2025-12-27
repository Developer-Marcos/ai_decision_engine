from pydantic import BaseModel, Field

class RelatorioExecutivo(BaseModel):
      veredito_final: str = Field(description="Decisão clara (Investir, Não Investir ou Cautela) acompanhada da pontuação final")
      percentual_score: float = Field(description="O percentual final de viabilidade calculado")
      detalhamento_notas: str = Field(description="Uma explicação textual sobre como as notas de mercado, financeira e técnica compuseram o resultado")
      sumario_executivo: str = Field(description="Resumo de alto nível para o investidor")
      analise_mercado: str = Field(description="Insights sobre demanda e concorrência")
      viabilidade_financeira: str = Field(description="Análise de custos e projeção de retorno")
      matriz_riscos: str = Field(description="Principais ameaças e pontos de atenção")
      conclusao_e_proximos_passos: str = Field(description="Ações recomendadas")