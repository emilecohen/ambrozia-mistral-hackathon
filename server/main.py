import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from os.path import join, dirname
from mistralai.client import MistralClient
from dotenv import load_dotenv
from mistralai.models.chat_completion import ChatMessage
from scraping_utils import scrape_website
from llm_utils import get_question_generator_prompt
from constants import SALESMAN_SYSTEM_PROMPT, SUMMARIZER_PROMPT
from pydantic import BaseModel


class ChatInput(BaseModel):
    prompt: str


class GenerateKnowledgeInput(BaseModel):
    url: str



load_dotenv(join(dirname(__file__), '.env'))
mistral_api_key = os.environ.get("MISTRAL_API_KEY")
client = MistralClient(api_key=mistral_api_key)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:63345",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat/complete")
async def complete(input: ChatInput):
    messages = [
        ChatMessage(role='system', content=SALESMAN_SYSTEM_PROMPT),
        ChatMessage(role='user', content=input.prompt)
    ]
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=messages,
    )
    return {"message": chat_response.choices[0].message.content}


@app.post("/generate-knowledge")
async def generate_knowledge(input: GenerateKnowledgeInput):
     content = scrape_website(input.url)
     messages = [ChatMessage(role='user', content=f"{SUMMARIZER_PROMPT} \n {content}")]
     chat_response = client.chat(
         model="mistral-large-latest",
         messages=messages,
     )
     return {"message": chat_response.choices[0].message.content}


@app.post("/generate-questions")
async def generate_questions(question: str, context: str):
    prompt = get_question_generator_prompt(question=question, context=context)
    messages = [ChatMessage(role='user', content=prompt)]
    chat_response = client.chat(
         model="mistral-large-latest",
         messages=messages,
    )
    return {"message": chat_response.choices[0].message.content}

