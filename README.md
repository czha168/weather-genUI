# weather-genUI
This is my porting of weather demo of [Generative UI Demos with FastHTML](https://github.com/kafkasl/genUI). Just to prove local LLM works.

# Dynamic Weather UI with FastHTML and Ollama

This project is a chat-based web application that generates dynamic, visual weather cards using a local Large Language Model (LLM) via Ollama. It demonstrates how to combine **FastHTML** for server-rendered UIs, **HTMX** for dynamic interactions, and **Ollama** for local LLM function calling (tool use).

## Features

*   **Local LLM Integration**: Uses Ollama to run the `gpt-oss:20b-128k` model locally.
*   **Dynamic UI**: The server generates HTML components (FastTags) which are seamlessly swapped into the page via HTMX.
*   **Function Calling**: The LLM uses a defined tool schema to return structured data, which the server converts into a visual weather card.
*   **MonsterUI Styling**: Clean, modern UI styling using the MonsterUI library.

## Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: You must have Ollama installed and running.
    *   [Download Ollama](https://ollama.com/)
3.  **Model**: You need to pull the specific model used in the script.
    ```bash
    ollama pull gpt-oss:20b-128k
    ```
    *(Note: You can edit the `model` variable in `main.py` to use any Ollama model that supports function calling, such as `llama3.1` or `mistral`).*

## Installation

1.  Clone this repository or download the source code.

2.  Install the required Python packages:
    ```bash
    pip install fasthtml monsterui ollama
    ```

## Usage

1.  **Start the Ollama Service** (if not already running):
    ```bash
    ollama serve
    ```

2.  **Run the Application**:
    ```bash
    python main.py
    ```

3.  **Access the App**:
    Open your browser and navigate to `http://localhost:5001` (or the port indicated in the terminal).

4.  **Interact**:
    *   Type a location into the chat input (e.g., "What's the weather in Tokyo?").
    *   The LLM will process the request, generate weather data for that location, and return a visual weather card.

## How It Works

### Architecture

The application follows a **Hypermedia-Driven Architecture**:

1.  **Frontend (FastHTML + HTMX)**:
    The UI is constructed entirely in Python using FastHTML components (`Div`, `H2`, `Form`, etc.). HTMX attributes (like `hx_post` and `hx_swap`) are added to HTML elements to enable dynamic behavior without writing JavaScript.

2.  **Backend (Ollama)**:
    When a message is sent, the server relays it to the local Ollama instance. A JSON schema (`tools_schema`) is provided to the LLM, defining the structure of a "Weather Component".

3.  **Tool Calling Flow**:
    *   **User Input**: "Weather in Paris"
    *   **LLM Response**: The LLM sees the available tool and returns a structured JSON object: `{"location": "Paris", "temperature": "18", "description": "cloudy"}`.
    *   **Server Execution**: The Python backend intercepts this "tool call," extracts the arguments, and executes the local `WeatherComponent` function.
    *   **UI Generation**: The function returns an HTML `Div` representing the weather card.
    *   **Response**: The server sends this HTML chunk back to the browser, where HTMX swaps it into the chat list.

### Key Components

*   `WeatherComponent`: A Python function that generates the HTML for the weather card. It also defines the schema used for LLM tool calling.
*   `ChatMessage`: A helper component that wraps text (or other components) in a chat bubble layout.
*   `send` (Route): The POST endpoint that handles the form submission, interacts with Ollama, and orchestrates the tool execution.

## Code Structure

```text
main.py
├── Imports & Setup
├── UI Components
│   ├── WeatherComponent()  # Generates the visual weather card
│   ├── ChatMessage()       # Generates chat bubbles
│   └── ChatInput()         # Manages the input field state
├── Routes
│   ├── index()             # Renders the initial page
│   └── send()              # Handles chat logic & Ollama integration
└── Tool Schema             # JSON definition of the tool for Ollama
```

## Customization

### Changing the Model
To use a different Ollama model, simply change the variable at the top of `main.py`:

```python
model = 'llama3.1'  # or 'mistral', 'codellama', etc.
```

### Modifying the Card
Edit the `WeatherComponent` function to change the visual layout, icons, or CSS classes. The changes will be reflected immediately in the next generated card.
