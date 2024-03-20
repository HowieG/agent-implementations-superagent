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
    name="Stock Assistant",
    description="An Assistant that can fetch stock prices",
    avatar="https://mylogo.com/logo.png",  # Replace with a real image
    is_active=True,
    llm_model="GPT_3_5_TURBO_16K_0613",
    initial_message="Hi there, how can I help you?",
    prompt="Use the Stock API to answer the users question."
)

client.agent.add_llm(agent_id=agent.data.id, llm_id=llm.data.id)

tool = client.tool.create(
    name="Stock API",
    description="Useful for answering questions about a specific stock",
    type="FUNCTION",
    return_direct=False,
    metadata={
        "functionName": "get-stock",
        "args": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker to search for"
            }
        }
    }
)

client.agent.add_tool(agent_id=agent.data.id, tool_id=tool.data.id)

prediction = client.agent.invoke(
    agent_id=agent.data.id,
    enable_streaming=False,
    input="What's the current stock price of Apple?",
    session_id="my_session_id"
)

output = prediction.data.get("output")
steps = prediction.data.get("intermediate_steps")

# Implementation of the get_stock function


def get_stock(ticker):
    print(f"Getting stock information for {ticker}")


# Create a dispatch table
tool_dispatch = {
    "get-stock": get_stock,
    # Add more tools here as needed
}

# Check the steps and run the function


def handle_tool_actions(steps):
    for item, _ in steps:
        tool_name = item.get('tool')
        tool_function = tool_dispatch.get(tool_name)
        if tool_function:
            tool_input = item.get('tool_input', {})
            tool_function(**tool_input)
        else:
            print(f"No function defined for tool: {tool_name}")


# Run your custom tool
handle_tool_actions(steps)
