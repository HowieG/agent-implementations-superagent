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
    name="Structured Assistant",
    description="An Assistant that returns responses in json",
    avatar="https://mylogo.com/logo.png",  # Replace with a real image
    is_active=True,
    initial_message="Hi there! How can I help you?",
    llm_model="GPT_4_1106_PREVIEW",
    prompt="Use the Browser to answer the user's question."
)

client.agent.add_llm(agent_id=agent.data.id, llm_id=llm.data.id)

tool = client.tool.create(
    name="Browser",
    description="useful for analyzing and summarizing websites and urls.",
    type="BROWSER"
)

client.agent.add_tool(agent_id=agent.data.id, tool_id=tool.data.id)

prediction = client.agent.invoke(
    agent_id=agent.data.id,
    input="List the top 5 articles on https://news.ycombinator.com.",
    enable_streaming=False,
    session_id="my_session_id",
    output_schema="[{title: string, points: number, url: string}]"  # Your desired output schema
)

print(prediction.data.get("output"))
