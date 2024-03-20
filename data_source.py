import os
from dotenv import load_dotenv
from superagent.client import Superagent


# Load environment variables from .env file
load_dotenv()

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

datasource = client.datasource.create(request={
    "name": "Tesla Q3 2023",
    "description": "Useful for answering questions about Teslas Q3 2023 earnings report",
    "type": "PDF",
    "url": "https://digitalassets.tesla.com/tesla-contents/image/upload/IR/TSLA-Q3-2023-Update-3.pdf"
})

# Connect the datasource the the Agent
client.agent.add_datasource(
    agent_id=agent.data.id,
    datasource_id=datasource.data.id
)

prediction = client.agent.invoke(
    agent_id=agent.data.id,
    input="What was Tesla's revenue?",
    enable_streaming=False,
    session_id="my_session_id"
)

print(prediction.data.get("output"))
