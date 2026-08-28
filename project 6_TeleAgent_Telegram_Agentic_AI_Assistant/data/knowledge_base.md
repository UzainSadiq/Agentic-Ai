# TeleAgent Knowledge Base

## Agentic AI
Agentic AI refers to systems that can interpret a goal, make decisions, use tools or external knowledge, and complete multi-step tasks. A simple chatbot generally maps a prompt directly to an answer, while an agent can decide what action should happen next.

## LangGraph
LangGraph is a framework for building stateful, multi-step agent workflows as graphs. A graph contains nodes that perform work and edges that determine how execution moves between nodes. This project uses nodes for analysis, tool execution, validation, and response generation.

## Tool Calling
Tool calling allows an AI system to select an operation such as a calculator, database query, API request, or search function. The application executes the operation and gives the result back to the model so it can produce a grounded response.

## Retrieval-Augmented Generation
RAG combines retrieval with generation. Instead of relying only on model memory, an application retrieves relevant information from a knowledge source and includes that evidence in the generation step. This project includes a lightweight local keyword retrieval layer to keep the demo simple and dependency-free.

## Telegram Bot
A Telegram bot is an application that receives messages through the Telegram Bot API and sends responses back to users. This project uses python-telegram-bot and polling so it can run locally without a public webhook server.

## Agent Validation
Validation is a separate workflow step that checks whether the selected tool or knowledge source returned usable evidence. This helps the agent avoid presenting an empty tool result as if it were a successful action.
