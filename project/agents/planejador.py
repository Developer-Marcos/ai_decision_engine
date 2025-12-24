from project.core.estado import AgentState
from project.config.llm_client import instanciar_llm
from project.utils.chains_auxiliares import gerar_meta_prompt
from pydantic import BaseModel, Field
from typing import List

class OutputPlanejador(BaseModel):
      plano: List[str] = Field(description="Tópicos que o relatório final deve cobrir")
      querys_de_pesquisa: List[str]

def node_planejador(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash-lite", agent_name="planejador", temperature=0.2)
      llm_estruturada = llm.with_structured_output(OutputPlanejador)

      diretrizes = gerar_meta_prompt(state["problema"])

      prompt=f"""
            <role>Analista de Decisões Estratégicas</role>
            
            <context>
            O usuário quer decidir: {state['problema']}
            </context>
            
            <dynamic_guidelines>
            {diretrizes}
            </dynamic_guidelines>
            
            <task>
            Com base no contexto e nas diretrizes acima, crie o plano de tópicos do relatório 
            e as queries de pesquisa para o Tavily.
            </task>
      """

      resposta = llm_estruturada.invoke(prompt)
      return {
            "plano": resposta.plano,
            "querys_de_pesquisa": resposta.querys_de_pesquisa,
            "numero_iteracao": 1
      }