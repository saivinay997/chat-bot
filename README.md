# Multi-LLM Chatbot

A versatile chatbot interface that supports multiple Language Learning Models (LLMs) including OpenAI's GPT-3.5, Google's Gemini Pro, and local LLMs through Ollama.

## Features

- Support for multiple LLM providers:
  - OpenAI GPT-3.5
  - Google Gemini Pro
  - Local LLMs via Ollama (e.g., Llama2)
- Chat history persistence
- Clean and modern UI using Streamlit
- Easy model switching
- Error handling and loading states

## Prerequisites

- Python 3.8+
- Ollama installed locally (for local LLM support)
- API keys for OpenAI and Google Gemini

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chat-bot.git
cd chat-bot
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Add your API keys to the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run chatgpt_ui.py
```

2. Select your preferred LLM from the sidebar dropdown
3. Start chatting!

## Note

- Make sure Ollama is running locally if you want to use local LLMs
- Keep your API keys secure and never commit them to version control
- The chat history is stored in session state and will be cleared when you refresh the page
