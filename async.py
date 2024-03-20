import os
from superagent.client import AsyncSuperagent

client = AsyncSuperagent(
    token=os.environ["SUPERAGENT_API_KEY"], # replace with your Superagent API key    
    base_url="https://api.beta.superagent.sh" # or you local environment
) 
