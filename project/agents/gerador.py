from project.core.estado import AgentState
from project.config.llm_client import instanciar_llm
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import List

class Viabilidade(BaseModel):
      nota: int = Field(description="Nota de 0 a 10 de viabilidade")
      justificativa: str = Field(description="Explicação detalhada baseada nos dados pesquisados")
      pontos_atencao: List[str] = Field(description="Riscos ou desafios identificados")

class ScoreIdeia(BaseModel):
      demanda_mercado: Viabilidade = Field(description="Avaliação do tamanho do público e dor que a ideia resolve")
      viabilidade_operacional_tecnica: Viabilidade = Field(description="Complexidade para construir/executar a solução (seja software, produto ou serviço)")
      viabilidade_financeira: Viabilidade = Field(description="Potencial de monetização, custos estimados e lucratividade")
      analise_competicao: Viabilidade = Field(description="Quem já faz algo similar e qual o diferencial proposto")
      veredito_final: str = Field(description="Resumo executivo recomendando ou não o investimento na ideia com os prós e contras")

def node_gerador(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash", agent_name="gerador", temperature=0.1)
      llm_estruturada = llm.with_structured_output(ScoreIdeia)

      prompt = f"""
            <persona>
                  Você é um Analista de Negócios Sênior e Estrategista de Go-to-Market.
                  Sua missão é avaliar a viabilidade técnica e comercial de uma proposta.
            </persona>

            <proposta_original>
                  {state['problema']}
                  </proposta_original>

                  <contexto_pesquisado>
                  {state['conteudo_pesquisado']}
            </contexto_pesquisado>

            <diretrizes_analise>
                  1. Identifique o modelo de negócio e adapte os critérios de avaliação.
                  2. Em 'Operacional/Técnica', avalie a complexidade de execução.
                  3. Baseie-se exclusivamente nos dados factuais fornecidos no contexto.
                  4. Se houver falta de informação, reporte em 'pontos_atencao'.
            </diretrizes_analise>
      """

      analise = llm_estruturada.invoke([HumanMessage(content=prompt)])
      relatorio_consolidado = f"""
            VEREDITO: {analise.veredito_final}

            DETALHAMENTO POR PILAR:
            - Mercado (Nota {analise.demanda_mercado.nota}): {analise.demanda_mercado.justificativa}
            - Técnica (Nota {analise.viabilidade_operacional_tecnica.nota}): {analise.viabilidade_operacional_tecnica.justificativa}
            - Financeira (Nota {analise.viabilidade_financeira.nota}): {analise.viabilidade_financeira.justificativa}
            - Competição (Nota {analise.analise_competicao.nota}): {analise.analise_competicao.justificativa}

            PONTOS DE ATENÇÃO GERAIS: {', '.join([item for pilar in [analise.demanda_mercado, analise.viabilidade_operacional_tecnica, analise.viabilidade_financeira, analise.analise_competicao] for item in pilar.pontos_atencao])}
      """

      media = (
            analise.demanda_mercado.nota +
            analise.viabilidade_operacional_tecnica.nota +
            analise.viabilidade_financeira.nota +
            analise.analise_competicao.nota
      ) / 4

      return {
            "notas_viabilidade": analise.model_dump(),
            "percentual_final": media*10,
            "relatorio_final": relatorio_consolidado
      }