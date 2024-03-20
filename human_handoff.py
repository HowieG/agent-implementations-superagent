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
    name="Human hand-off",
    description="Useful when the user wants to speak to a human operator",
    type="HAND_OFF"
)

# Add the tool to your agent
client.agent.add_tool(agent_id=agent.data.id, tool_id=tool.data.id)

# Write a helper function that checks for human hand-off


def check_for_human_handoff(data: list) -> bool:
    for item, _ in data:
        if item['tool'] == 'human-hand-off':
            return True
    return False


prediction = client.agent.invoke(
    agent_id=agent.data.id,
    enable_streaming=False,
    input="I want to speak to a human",
    session_id="my_session_id"
)

output = prediction.data.get("output")
steps = prediction.data.get("intermediate_steps")

if check_for_human_handoff(steps):
    # Run any local code here
    print("HUMAN HANDOFF DETECTED")
