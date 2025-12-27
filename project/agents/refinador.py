from project.config.llm_client import instanciar_llm
from project.core.estado import AgentState
from project.utils.schema_refinador import RelatorioExecutivo

def node_refinador(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash", agent_name="refinador", temperature=0.2)
      llm_estruturada = llm.with_structured_output(RelatorioExecutivo)

      instrucoes = state.get("instrucoes_refinamento")

      if not instrucoes or instrucoes.strip() == "":
            diretriz_final = "Siga o padrão de relatório executivo padrão, focando em clareza e um veredito direto ao ponto."
      else:
            diretriz_final = f"Siga rigorosamente estas prioridades apontadas pelo investidor: {instrucoes}"

      prompt = f"""
            <role>Especialista em Comunicação Executiva e Design de Informação</role>
            
            <contexto>
                  Você recebeu um relatório bruto de viabilidade e deve polir para a entrega final.
                  Problema: {state['problema']}
                  Score Calculado: {state['percentual_final']}%
                  Notas: {state['notas_viabilidade']}       
            </contexto>

            <conteudo_bruto>
                  {state['relatorio_final']}
            </conteudo_bruto>

            <diretriz_de_estilo>
                  {diretriz_final}
            </diretriz_de_estilo>

            <missao>
                  Organize os dados brutos no formato estruturado solicitado.
                  No 'veredito_final', integre a pontuação de {state['percentual_final']}% com a recomendação (Investir/Não Investir/Cautela).
                  No 'detalhamento_notas', explique os valores: {state['notas_viabilidade']} em tópicos.
            </missao>
 
            Gere o relatório final polido:
      """

      resposta = llm_estruturada.invoke(prompt)

      return {"relatorio_final": resposta}