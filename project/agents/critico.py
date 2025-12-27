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
            <role>
                  Você é um Mentor de Negócios e Analista de Riscos. 
                  Sua missão é garantir que o relatório final reduza a incerteza para uma decisão de investimento.
            </role>

            <contexto_de_decisao>
                  O usuário quer decidir sobre: {state['problema']}
                  Relatório atual: {state['relatorio_final']}
            </contexto_de_decisao>

            <logica_de_roteamento>
                  Você deve decidir o 'destino' com base na natureza da falha:
                  
                  1. Mande para o 'pesquisador' quando:
                  - O plano está bom, mas faltam dados factuais (ex: preços, concorrência local, valores de aluguel).
                  - Os dados atuais são genéricos e precisam de números específicos do mundo real.

                  2. Mande para o 'planejador' quando:
                  - A estratégia proposta parece errada ou incompleta (ex: ignorou impostos, esqueceu custos de marketing, ou o modelo de negócio não faz sentido).
                  - O foco da pesquisa está no lugar errado (ex: pesquisando padaria de luxo em bairro de baixa renda).
                  - É necessário REESCREVER os tópicos do plano para abordar o problema por outro ângulo.

                  3. Mande para o 'refinador' quando:
                  - As lacunas restantes são aceitáveis para um estudo preliminar e os dados fundamentais já estão lá.
                  - Se escolher este destino, use o campo 'instrucoes_de_correcao' para dizer ao Refinador como ele deve formatar este relatório (ex: 'Destaque a tabela de custos operacionais' ou 'Enfatize a análise da concorrência em Madureira').
            </logica_de_roteamento>

            <instrucoes_de_ouro>
                  - Seja Específico: No campo 'instrucoes_de_correcao', se enviar para o Planejador, diga: "Adicione o tópico X ao plano". Se enviar para o Pesquisador, dê a query pronta.
                  - Rigor Amigável: Substitua termos agressivos por "necessidade de evidência".
            </instrucoes_de_ouro>
      """

      decisao = llm_estruturada.invoke([HumanMessage(content=prompt)])

      retorno = {
            "proximo_passo": decisao.destino,
            "iteracao_critica": 1,
            "feedback_critico": "",
            "instrucoes_refinamento": ""
      }

      if decisao.destino == "refinador":
            retorno["instrucoes_refinamento"] = decisao.instrucoes_de_correcao
      else:
            retorno["feedback_critico"] = f"[{decisao.destino.upper()}] {decisao.critica_detalhada} | Ação: {decisao.instrucoes_de_correcao}"
     
      return retorno