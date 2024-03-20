import os
from superagent.client import Superagent

client = Superagent(
    token=os.environ["SUPERAGENT_API_KEY"],  # replace with your Superagent API
    base_url="https://api.beta.superagent.sh"  # or your local environment
)
