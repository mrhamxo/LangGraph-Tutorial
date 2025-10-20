# 🔗 LangGraph Tutorial: Building AI Workflows

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-v0.1+-green.svg)](https://github.com/langchain-ai/langchain)

A comprehensive tutorial and example repository for building stateful AI workflows using LangGraph.

## 📚 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Available Notebooks](#Available-Notebooks)
- [License](#license)

## 🎯 About

LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with the ability to create cyclical graphs, which are essential for building agent-like behaviors.

This repository provides:
- 📖 Step-by-step tutorials
- 💡 Practical examples
- 🛠️ Ready-to-use templates
- 📊 Real-world use cases

## ✨ Features

- **Basic Workflows**: Simple state management and graph construction
- **LLM Integration**: Connect language models to your workflows
- **Conditional Routing**: Dynamic branching based on state
- **Tool Integration**: Function calling and external API integration
- **Persistence**: Checkpoint and resume workflows
- **Chatbot Examples**: Build conversational AI applications
- **Multi-Agent Systems**: Coordinate multiple AI agents

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/langgraph-tutorial.git
cd langgraph-tutorial
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Required Dependencies

```txt
langgraph>=0.0.1
langchain>=0.1.0
langchain-groq>=0.0.1
langchain-community>=0.0.1
python-dotenv>=1.0.0
```

## Available Notebooks

| Notebook | Description | Level |
|----------|-------------|-------|
| `BMI_workflow_1.ipynb` | BMI Calculator workflow | Beginner |
| `llm_workflow_2.ipynb` | LLM integration basics | Beginner |
| `batsman_workflow_4.ipynb` | Cricket stats calculator | Intermediate |
| `essay_workflow_5.ipynb` | Essay evaluation system | Intermediate |
| `X_post_generator_8.ipynb` | Social media post generator | Advanced |
| `basic_chatbot_9.ipynb` | Simple chatbot implementation | Intermediate |
| `fault_tolerance_11.ipynb` | Error handling and recovery | Advanced |
| `tools_12.ipynb` | Tool integration with LLMs | Advanced |

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Example Notebooks](https://github.com/langchain-ai/langgraph/tree/main/examples)
