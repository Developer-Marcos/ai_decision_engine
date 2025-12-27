from project.core.estado import AgentState
from project.config.llm_client import instanciar_llm
from project.utils.chains_auxiliares import gerar_meta_prompt
from pydantic import BaseModel, Field
from typing import List

class OutputPlanejador(BaseModel):
      plano: List[str] = Field(description="Tópicos que o relatório final deve cobrir")
      querys_de_pesquisa: List[str]

def node_planejador(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash", agent_name="planejador", temperature=0.2)
      llm_estruturada = llm.with_structured_output(OutputPlanejador)

      diretrizes = gerar_meta_prompt(state["problema"])

      feedback = state.get("feedback_critico", "")

      contexto_de_ajuda = ""
      if feedback:
            contexto_de_ajuda = f"""
                  <analise_rejeitada_anterior>
                        {state.get('relatorio_final', 'Nenhuma análise gerada ainda.')}
                  </analise_rejeitada_anterior>

                  <feedback_do_critico>
                  {feedback}
                  </feedback_do_critico>
                  
                  INSTRUÇÃO DE LIMPEZA: Esqueça os dados brutos anteriores. Foque em criar queries 
                  que busquem o que falta nesta análise acima, conforme as instruções do Crítico.
            """

      prompt=f"""
            <role>Analista de Decisões Estratégicas</role>
            
            <context>
            O usuário quer decidir: {state['problema']}
            </context>

            {contexto_de_ajuda}
            
            <dynamic_guidelines>
            {diretrizes}
            </dynamic_guidelines>
            
            <task>
            Com base no contexto, nas diretrizes no feedback (se houver), crie o plano de tópicos 
            e as novas queries de pesquisa para o Tavily que tragam dados mais profundos.
            </task>
      """

      resposta = llm_estruturada.invoke(prompt)
      return {
            "plano": resposta.plano,
            "querys_de_pesquisa": resposta.querys_de_pesquisa,
            "iteracao_critica": 1,
            "iteracao_pesquisa": -state.get("iteracao_pesquisa", 0),
            "feedback_critico": ""
      }