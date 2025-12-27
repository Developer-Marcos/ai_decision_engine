from project.config.llm_client import instanciar_llm
from project.core.estado import AgentState
from pydantic import BaseModel, Field

class AnaliseGuardrail(BaseModel):
      aprovado: bool = Field(description="True se o tema for sobre negócios, investimentos ou viabilidade. False se for antiético, perigoso ou totalmente fora do escopo.")
      motivo_rejeicao: str = Field(description="Explicação concisa caso a pergunta seja bloqueada.")

def node_guardrail(state: AgentState):
      llm = instanciar_llm(modelo="gemini-2.5-flash-lite", agent_name="seguranca", temperature=0)
      llm_estruturada = llm.with_structured_output(AnaliseGuardrail)

      prompt = f"""
            Você é um Filtro de Segurança e Escopo. 
            Analise a intenção do usuário: "{state['problema']}"

            CRITÉRIOS DE BLOQUEIO:
            1. Atividades ilegais ou antiéticas.
            2. Discurso de ódio ou conteúdo sexual.
            3. Perguntas que não têm relação com negócios, produtos, serviços ou investimentos.

            Se for aprovado, retorne aprovado=True. 
            Se for bloqueado, retorne aprovado=False e explique o porquê.
      """

      verificacao = llm_estruturada.invoke(prompt)

      if not verificacao.aprovado:
            return {
                  "aprovado": False,
                  "relatorio_final": f"BLOQUEIO DE SEGURANÇA: {verificacao.motivo_rejeicao}",
                  "proximo_passo": "end"
            }
      
      return {"aprovado": True, "proximo_passo": "planejador"}