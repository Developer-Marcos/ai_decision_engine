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
                  Organize os dados brutos no formato estruturado solicitado (Pydantic).
                        
                  1. 'veredito_final': Uma frase de impacto começando com o status (Investir/Não Investir/Cautela) seguido do score {state['percentual_final']}% e justificativa curta.
                  2. 'detalhamento_notas': Transforme as notas {state['notas_viabilidade']} em uma LISTA de strings. Cada item deve seguir o padrão: "Pilar (Nota X): Explicação concisa".
                  3. 'matriz_riscos': Extraia uma LISTA de strings com as principais ameaças, sem parágrafos longos.
                  4. 'conclusao_e_proximos_passos': Transforme as recomendações em uma LISTA de ações práticas e sequenciais.
            </missao>

            Gere o relatório final polido seguindo rigorosamente a estrutura de listas para os campos de notas, riscos e conclusões:
      """

      resposta = llm_estruturada.invoke(prompt)

      return {"relatorio_final": resposta}