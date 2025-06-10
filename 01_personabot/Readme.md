# Persona AI Bot – Hitesh Choudhary Edition

A GenAI-powered chatbot that mimics the personality, tone, and style of **Hitesh Choudhary**, a renowned tech YouTuber and educator. This bot is trained on his **recent Twitter posts** and interacts with users in a way that reflects his knowledge, humor, and teaching style.

---

## Features

- 🧠 **Persona Cloning**: Emulates Hitesh’s tech-focused, motivational, and humorous personality.

- 💬 **Interactive Conversations**: Responds to coding questions, beginner doubts, and motivational queries like Hitesh would.

- 🐍 **Python-Based CLI Interface**: Simple command-line chat experience.

- 🧵 **Twitter-based Personality Model**: Built using recent tweets as examples for prompt engineering or fine-tuning.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/GenAI-Projects.git
cd GenAI-Projects/01_personabot
```

### 2. Set Up Environment

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Add `.env` File

Create a `.env` file in the root directory with your API key (if using OpenAI or any LLM):

```env
OPENAI_API_KEY=your_api_key_here
```

> ✅ Make sure `.env` is added to `.gitignore` so it’s not pushed to GitHub.

---

## Project Structure

```
01_personabot/
│
├── persona.py            # Main chatbot script
├── examples.json         # Example tweets and personality responses
├── .env                  # API keys and config (ignored from Git)
└── README.md             # Documentation
```

---

## How It Works

- Parses Hitesh’s recent tweets and builds a **prompt template** based on his style.

- Sends user queries + personality context to a Gemini 2.5-flash.

- Returns answers that sound like Hitesh: tech-savvy, direct, slightly sarcastic, and educational.

---

## Customization

Want to swap out Hitesh for another tech creator? Just update the:

```
System_Prompt inside persona.py
```

---

## Ethical Note

This bot is a **fan-made project** for educational use and is **not officially associated with Hitesh Choudhary**. Please use respectfully.

---

## Sample Interaction

```
User: Hellp
Bot (Hitesh): Haanji, Kaise hain aap. Kya help karu aapki?
```

---

## Credits

Created by Atishay Kumar Pandey as part of the GenAI Projects series.\
Persona inspired by [Hitesh Choudhary](https://x.com/Hiteshdotcom)