from project.config.llm_client import instanciar_llm
from langchain_core.messages import HumanMessage
from project.core.estado import AgentState
from pydantic import BaseModel, Field
from typing import Literal

class AnaliseCritica(BaseModel):
      aprovado: bool = Field(description="Indica se o relatório está pronto para o cliente final")
      destino: Literal["refinador", "pesquisador", "planejador"] = Field(
            description="Para onde o fluxo deve ir: 'refinador' se aprovado; 'pesquisador' se faltar dado factual; 'planejador' se a estratégia estiver errada"
      )
      critica_detalhada: str = Field(description="Análise ácida sobre o que falta ou o que está errado")
      instrucoes_de_correcao: str = Field(description="Comandos claros para o próximo agente agir")

def node_critico(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash", agent_name="critico", temperature=0.4)
      llm_estruturada = llm.with_structured_output(AnaliseCritica)

      prompt = f"""
            <persona>
                  Você é um Investidor Senior e Crítico de Negócios. Seu papel é garantir a qualidade. Se os dados forem insuficientes, aponte o que falta de forma construtiva. Se a análise for aceitável como um estudo preliminar, aprove-a com ressalvas.
            </persona>

            <analise_a_ser_criticada>
                  {state['relatorio_final']}
                  Notas: {state['notas_viabilidade']}
            </analise_a_ser_criticada>

            <contexto_da_pesquisa>
                  {state['conteudo_pesquisado']}
            </contexto_da_pesquisa>

            <instrucoes>
                  1. Se a análise ignorou riscos óbvios ou dados financeiros, REPROVE.
                  2. Se faltar apenas um dado pontual (ex: preço de um concorrente) ou alguns dados pontuais, envie para o 'pesquisador'.
                  3. Se o plano de pesquisa foi mal executado ou a lógica de negócio está falha, envie para o 'planejador'.
                  4. Só aprove e envie para o 'refinador' se você investiria seu próprio dinheiro nessa análise.
            </instrucoes>
      """

      decisao = llm_estruturada.invoke([HumanMessage(content=prompt)])

      return {
            "feedback_critico": f"[{decisao.destino.upper()}] {decisao.critica_detalhada} | Ação: {decisao.instrucoes_de_correcao}",
            "proximo_passo": decisao.destino
      }
     