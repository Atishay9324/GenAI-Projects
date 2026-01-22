# 🌐 AI Website Builder

Build stunning websites using AI agents powered by LangChain and OpenAI.

## ✨ Features

- **Multi-Agent Architecture**: 4 specialized AI agents work together
  - 📝 **Content Agent**: Generates compelling website copy
  - 🎨 **Designer Agent**: Creates beautiful design specifications
  - 💻 **Coder Agent**: Writes clean HTML/CSS/JavaScript
  - 🔍 **Reviewer Agent**: Polishes and improves the final code

- **Interactive CLI**: User-friendly command-line interface with prompts
- **Multiple Styles**: Choose from modern, minimal, bold, elegant, or playful
- **Built-in Preview**: Instantly preview your generated website
- **Production-Ready Output**: Responsive, accessible, SEO-friendly code

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
copy .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your-actual-api-key-here
```

### 3. Build Your Website

**Interactive Mode:**
```bash
python -m website_builder build -i
```

**Direct Mode:**
```bash
python -m website_builder build -d "A modern portfolio for a photographer" -t portfolio -s modern
```

## 📖 Commands

### `build` - Create a New Website

```bash
python -m website_builder build [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `-d, --description` | Website description |
| `-t, --type` | Type: business, portfolio, landing, blog, saas |
| `-s, --style` | Style: modern, minimal, bold, elegant, playful |
| `-n, --name` | Output folder name |
| `--skip-review` | Skip the code review step |
| `-i, --interactive` | Use interactive prompts |

### `preview` - Preview a Website

```bash
python -m website_builder preview output/my-website
```

### `config` - Show Configuration

```bash
python -m website_builder config
```

## 📁 Project Structure

```
02_Website-Builder/
├── website_builder/
│   ├── __init__.py
│   ├── __main__.py        # Entry point
│   ├── cli.py             # CLI interface
│   ├── config.py          # Configuration
│   ├── orchestrator.py    # Agent coordination
│   └── agents/
│       ├── base.py        # Base agent class
│       ├── content.py     # Content generation
│       ├── designer.py    # Design specifications
│       ├── coder.py       # Code generation
│       └── reviewer.py    # Code review
├── output/                 # Generated websites
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ How It Works

1. **Content Agent** analyzes your description and generates structured content (headlines, about text, features, etc.)

2. **Designer Agent** creates design specifications (colors, typography, spacing, effects)

3. **Coder Agent** combines content and design to generate complete HTML/CSS/JS

4. **Reviewer Agent** polishes the code for better accessibility, SEO, and performance

## 📝 Example

```bash
python -m website_builder build -d "A SaaS landing page for an AI writing assistant that helps bloggers create content faster" -t saas -s modern -n ai-writer
```

This generates a complete website in `output/ai-writer/`.

## ⚙️ Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | Model to use | gpt-4o-mini |

## 📄 License

MIT License
