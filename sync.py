import os
from superagent.client import Superagent

client = Superagent(
    token=os.environ["SUPERAGENT_API_KEY"],
    base_url="https://api.beta.superagent.sh"
)

llm = client.llm.create(request={
    "provider": "OPENAI",
    "apiKey": os.environ["OPENAI_API_KEY"]
})

agent = client.agent.create(
    name="Chat Assistant",
    description="My first Assistant",
    type="SUPERAGENT",
    avatar="https=//myavatar.com/homanp.png",
    is_active=True,
    initial_message="Hi there! How can I help you?",
    llm_model="GPT_3_5_TURBO_16K_0613",
    prompt="You are a helpful AI Assistant",
)

client.agent.add_llm(agent_id=agent.data.id, llm_id=llm.data.id)

response = client.agent.invoke(
    agent_id=agent.data.id,
    input="What was Tesla's revenue?",
    enable_streaming=False,
    session_id="my_session_id",
    llm_params={"temperature": 0.0, "max_tokens": 100}
)

print(response.data.get("output"))
