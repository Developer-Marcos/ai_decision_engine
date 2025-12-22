from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Dict, Any

def instanciar_llm(agent_name: str, *, temperature: float = 0.3, extra_metadata: Optional[Dict[str, Any]] = None):
      metadata = {
            "agent": agent_name,
      }

      if extra_metadata:
            metadata.update(extra_metadata)
      
      return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=temperature,
            metadata=metadata,
      )