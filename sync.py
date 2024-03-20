import os
from superagent.client import Superagent

client = Superagent(
    token=os.environ["SUPERAGENT_API_KEY"],  # replace with your Superagent API
    base_url="https://api.beta.superagent.sh"  # or your local environment
)

llm = client.llm.create(request={
    "provider": "OPENAI",
    "apiKey": os.environ["OPENAI_API_KEY"]
})

agent = client.agent.create(request={
    "name": "Chat Assistant",
    "description": "My first Assistant",
    "type": "SUPERAGENT",
    "avatar": "https://myavatar.com/homanp.png",
    "isActive": True,
    "initialMessage": "Hi there! How can I help you?",
    "llmModel": "GPT_3_5_TURBO_16K_0613",
    "prompt": "You are a helpful AI Assistant",
})

client.agent.add_llm(agent_id=agent.data.id, llm_id=llm.data.id)

prediction = client.agent.invoke(
    agent_id=agent.data.id,
    input="Hi there!",
    enable_streaming=False,
    session_id="my_session"  # Best practice is to create a unique session per user
)

print(prediction.data.get("output"))

# Hello there, how can I help you?
