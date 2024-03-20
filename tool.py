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
    description="An Assistant that has access to the Browser tool",
    avatar="https://mylogo.com/logo.png",  # Replace with a real image
    is_active=True,
    initial_message="Hi there! How can I help you?",
    llm_model="GPT_3_5_TURBO_16K_0613",
    prompt="Use the Browser to answer the user's question."
)

client.agent.add_llm(agent_id=agent.data.id, llm_id=llm.data.id)

tool = client.tool.create(
    name="Browser",
    description="A portal to the internet, useful for answering questions about websites or urls.",
    type="BROWSER",
    # metadata={"key": "value"} Optional metadata for the tool.
    return_direct=False  # return_direct is required while creating a tool.
)

client.agent.add_tool(agent_id=agent.data.id, tool_id=tool.data.id)

prediction = client.agent.invoke(
    agent_id=agent.data.id,
    input="Summarize superagent.sh",
    enable_streaming=False,
    session_id="my_session_id",
)

print(prediction.data.get("output"))
