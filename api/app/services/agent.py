# # differ btw inheritence --- inherit with base class it's stronge relationship (is a relationship)
# # association -- weak relationship (has a relationship)
# # 2 type of association :  1. composition (strong bond)  2. aggregation kisi cheez ko bad ma use kerna (weak bond)
# # conversational loop ----> aik ans phir jawab
# #agentic loop --> react pattern

# # tool : in tools has 3 thing : function name, signature , return type agrument perhi hoti context window(these are function defination)
# # and for llm the most importent thing is doc string(jo triple double cout hota hy """)





# #self.rag is instence attribute class type if their is any integer then int type

#                  # content mean  3 chunks ka content jo llm ky pass jaye ga
#                                                              # artifact : the information that does not need it the user thing


from langchain.agents import create_agent
from langchain.messages import HumanMessage, ToolMessage
from pydantic import BaseModel
from app.core.config import get_settings
from app.prompt.loader import get_prompt
from app.llm.models import get_chat_model
from app.rag.vector_store import get_vector_store
from app.tools.knowledge.handbook import Source, file_search
from app.middleware.stack import default_stack


class Answer(BaseModel):
    answer: str
    sources: list[Source]


class ClauseAgent:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.store = get_vector_store(self.settings)

        self.agent = create_agent(
            model=get_chat_model(self.settings),
            tools=[file_search(self.store, self.settings.top_k)],
            system_prompt=get_prompt(
                name="support/system",
                version=self.settings.system_prompt_version,
            ),
             middleware=default_stack(self.settings),
            checkpointer=checkpointer
        )

    def ask(self, question: str) -> Answer:
        result = self.agent.invoke({"messages": [HumanMessage(question)]})
        messages = result["messages"]

        sources: list[Source] = []
        for msg in messages:
            if isinstance(msg, ToolMessage) and isinstance(msg.artifact, list):
                sources.extend(msg.artifact)

        return Answer(answer=messages[-1].text, sources=sources)

    def close(self) -> None:
        if hasattr(self.store, "client") and hasattr(self.store.client, "close"):
            self.store.client.close()
