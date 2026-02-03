from __future__ import annotations

from dataclasses import dataclass

from langchain_clis.shared.model import ModelConfig


@dataclass(frozen=True)
class LlmClient:
    model: object

    @staticmethod
    def from_config(cfg: ModelConfig) -> "LlmClient":
        if cfg.provider != "openai":
            raise RuntimeError(f"Unsupported provider: {cfg.provider}")

        # Lazy import so `--help` and `--dry-run` work without LangChain installed.
        from langchain_openai import ChatOpenAI  # type: ignore

        model = ChatOpenAI(model=cfg.model, temperature=cfg.temperature)
        return LlmClient(model=model)

    def complete(self, *, system: str, user: str) -> str:
        from langchain_core.messages import HumanMessage, SystemMessage  # type: ignore

        messages = [SystemMessage(content=system), HumanMessage(content=user)]
        result = self.model.invoke(messages)
        content = getattr(result, "content", None)
        if not isinstance(content, str):
            raise RuntimeError("Model returned non-text content.")
        return content
