!pip install gradio
!pip install openai
!pip install langchain

import os
import gradio as gr
from openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set OpenRouter API Key
OPENROUTER_API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

# Initialize OpenRouter client
client = OpenAI(base_url=BASE_URL, api_key=OPENROUTER_API_KEY)

# Chatbot Prompt Template
template = """Meet Riya, your youthful and witty personal assistant! At 21 years old, she's full of energy and always eager to help. 
Riya's goal is to assist you with any questions or problems you might have. Her enthusiasm shines through in every response, 
making interactions with her enjoyable and engaging.

{chat_history}
User: {user_message}
Chatbot:"""

prompt = PromptTemplate(input_variables=["chat_history", "user_message"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history")

# Function to generate chatbot responses
def get_text_response(user_message, history):
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat:free",  # Switched to a faster model
        temperature=0.2,
        max_tokens=100,
        messages=[{"role": "user", "content": user_message}],
        extra_headers={
            "HTTP-Referer": "https://yourwebsite.com",  # Optional ranking info
            "X-Title": "Riya - AI Assistant",
        }
    )
    return completion.choices[0].message.content

# Gradio Chat Interface
demo = gr.ChatInterface(get_text_response, examples=[
    "How are you doing?", 
    "What are your interests?", 
    "Which places do you like to visit?"
])

# Launch the chatbot
if __name__ == "__main__":
    demo.launch()
