from typing import List, Dict
import os
import asyncio
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()

class LLMService:
    def __init__(self, use_azure=False, azure_config=None):
        self.use_azure = use_azure
        self.azure_config = azure_config or {
            'api_key': os.getenv("AZURE_OPENAI_API_KEY"),
            'endpoint': os.getenv("AZURE_OPENAI_ENDPOINT"),
            'deployment_name': os.getenv("AZURE_DEPLOYMENT_NAME")
        }

        if self.use_azure:
            self.openai_client = AzureChatOpenAI(
                azure_endpoint=self.azure_config['endpoint'],
                azure_deployment=self.azure_config['deployment_name'],
                api_key=self.azure_config['api_key'],
                api_version="2024-02-15-preview"
            )
        else:
            self.openai_client = ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-3.5-turbo"
            )

        self.gemini_client = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-002",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def format_chat_history(self, messages: List[Dict]) -> List:
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "system":
                formatted_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_messages.append(AIMessage(content=msg["content"]))
        return formatted_messages

    async def get_openai_response(self, messages: List[Dict]) -> str:
        formatted_messages = self.format_chat_history(messages)
        response = await self.openai_client.ainvoke(formatted_messages)
        return response.content

    async def get_gemini_response(self, messages: List[Dict]) -> str:
        formatted_messages = self.format_chat_history(messages)
        response = await self.gemini_client.ainvoke(formatted_messages)
        return response.content

    def get_ollama_response(self, messages: List[Dict], model: str = "llama2") -> str:
        conversation = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages if msg["role"] != "system"
        ]
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={"model": model, "messages": conversation},
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to get response from Ollama. {str(e)}"

    async def get_response(self, model: str, messages: List[Dict]) -> str:
        if model.lower() == "openai":
            return await self.get_openai_response(messages)
        elif model.lower() == "gemini":
            return await self.get_gemini_response(messages)
        elif model.lower() == "ollama":
            return self.get_ollama_response(messages)
        else:
            return "Error: Invalid model selection."
