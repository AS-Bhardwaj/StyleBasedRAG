from openai import OpenAI
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(openai_api_key)

client.embeddings(model='')
