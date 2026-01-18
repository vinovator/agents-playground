# Agents Playground

Welcome to the **Agents Playground**! This repository is a collection of experiments and patterns using modern Agentic AI frameworks. It serves as a sandbox for exploring interactions between LLMs, tools, and autonomous workflows.

## 📂 Repository Structure

### [CrewAI](./crewai/)
Experiments with **CrewAI** for orchestrating role-based autonomous agents.
- **Event Automation**: Agents coordinating to plan events.
- **Startup Validator**: Hierarchical crews validating business ideas.
- **Financial Analysis**: Collaborative financial research.
- **Customer Outreach**: Automated campaign strategies.
- **Six Thinking Hats**: Decision making framework using agents.
- **Notebooks**: Comprehensive tutorials (`crewai_basics.ipynb`, `crewai_async_tasks.ipynb`, etc).

### [PydanticAI](./PydanticAI/)
Examples using **PydanticAI** for strictly typed, production-grade agents.
- **FastAPI Server**: A REST API wrapping an agent with context injection and structured outputs.
- **Streaming Legal Analyst**: A real-time contract analysis tool using Server-Sent Events (SSE) and structured output streams.
- **Human-in-Loop Refund Agent**: A sophisticated agent with state persistence, pausing/resuming execution for human approval on high-value transactions.

### [LangGraph](./LangGraph/)
Workflows built with **LangGraph** for stateful, graph-based agent applications.
- **Debate Dojo**: Two agents debating a topic.

### [Semantic Kernel](./SemanticKernel/)
Experiments using Microsoft's **Semantic Kernel**.
- **Polygot Bot**: A multi-language interaction bot example.
- **Smart Home Bot**: An agent using plugins to control simulated smart devices.
- **Human-in-Loop Refund Agent**: An agent demonstrating state management and human intervention flows.

### Basic Examples
Simple standalone notebooks for testing connectivity and basic models.
- **Ollama Call**: `simple_ollama_call.ipynb`
- **OpenAI Call**: `simple_openai_call.ipynb`

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Conda](https://docs.conda.io/en/latest/) (optional but recommended)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd "Agents Playground"
    ```

2.  **Install Dependencies**:
    It is recommended to create a virtual environment first.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**:
    Create a `.env` file in the root directory (or respective sub-directories) with your API keys.
    ```env
    OPENAI_API_KEY=sk-...
    GOOGLE_API_KEY=...
    ANTHROPIC_API_KEY=...
    ```

### Running Examples

**Jupyter Notebooks**:
Start the notebook server to explore interactive examples:
```bash
jupyter notebook
```

**FastAPI Server**:
Navigate to the PydanticAI server directory:
```bash
cd PydanticAI/fastapi-pydanticai-server
uvicorn main:app --reload
```

## 🛠 Frameworks Used

- **[CrewAI](https://docs.crewai.com/)**: Orchestrating role-playing agents.
- **[LangGraph](https://python.langchain.com/docs/langgraph)**: Building stateful, multi-actor applications with LLMs.
- **[PydanticAI](https://ai.pydantic.dev/)**: Building production grade agents with Pydantic.
- **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)**: Integration of LLMs with existing code.
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern web framework for building APIs.
