from langchain.agents.middleware import (
    AgentMiddleware,
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    ToolCallLimitMiddleware,
    SummarizationMiddleware,
    ClearToolUsesEdit, ContextEditingMiddleware
)

from app.core.config import Settings
from app.llm.models import get_chat_model


def default_stack(settings: Settings) -> list[AgentMiddleware]:
    stack = [
    ModelCallLimitMiddleware(run_limit=settings.max_model_call, exit_behavior="end"),
    ToolCallLimitMiddleware(run_limit=settings.max_model_call),
    SummarizationMiddleware(
    model=get_chat_model(settings),
    trigger=("tokens",3000),
    keep=("messages",10),
    summary_prompt=""

    )
    ]



fallback = get_fallback_models(Settings)
if fallback:
    
