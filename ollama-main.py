from fasthtml.common import *
from monsterui.all import *
import ollama  # Changed from claudette
from datetime import datetime
import json

hdrs = Theme.blue.headers()

# Create your app with the theme
app, rt = fast_app(hdrs=hdrs)

model = 'gpt-oss:20b-128k'

# Define the weather component function with enhanced visuals
def WeatherComponent(location:str, temperature:str, description:str):
    """Generate a clean, minimal weather card like iPhone's weather app.
    Description should be 'sunny', 'cloudy', or 'rainy'."""
    
    # Simple weather icons (minimalist approach)
    weather_icons = {
        "sunny": "https://cdn-icons-png.flaticon.com/512/869/869869.png",
        "cloudy": "https://cdn-icons-png.flaticon.com/512/414/414825.png",
        "rainy": "https://cdn-icons-png.flaticon.com/512/3351/3351979.png"
    }
    
    # Get image and determine background color
    desc_lower = description.lower()
    img_url = next((url for condition, url in weather_icons.items() 
                 if condition in desc_lower), weather_icons["sunny"])
    
    # Get current date
    current_date = datetime.now().strftime("%A, %B %d")
    
    return Div(
        H2(location, cls="text-xl font-semibold mb-1"),
        Div(cls="flex justify-between items-center mb-3")(
            P(current_date, cls="text-sm font-medium"),
            P(description.capitalize(), cls="text-sm font-medium")
        ),
        Div(cls="flex items-center")(
            Span(f"{temperature}°", cls="text-7xl font-light mr-4"),
            Img(src=img_url, cls="w-16 h-16")
        ),
        cls="p-4 bg-sky-500 text-white rounded-lg max-w-xs"
    )

# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}")(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(msg, cls=f"chat-bubble {bubble_class}"),
               Hidden(msg, name="messages")
           )

# The input field for the user message.
def ChatInput():
    return Input(name='msg', id='msg-input', placeholder="Type a message",
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.get
def index():
    page = Form(hx_post=send, hx_target="#chatlist", hx_swap="beforeend")(
           Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
               Div(cls="flex space-x-2 w-full")(
                   ChatInput(),
                   Button("Send", cls="btn btn-primary")
               )
           )
    return Titled('Weather Component', page, cls=ContainerT.sm)

# Define the tool schema for Ollama
tools_schema = [{
    'type': 'function',
    'function': {
        'name': 'WeatherComponent',
        'description': "Generate a clean, minimal weather card like iPhone's weather app. Description should be 'sunny', 'cloudy', or 'rainy'.",
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {'type': 'string', 'description': 'The city name'},
                'temperature': {'type': 'string', 'description': 'The temperature value (e.g. 72)'},
                'description': {'type': 'string', 'description': "Weather condition: 'sunny', 'cloudy', or 'rainy'"}
            },
            'required': ['location', 'temperature', 'description']
        }
    }
}]

# Handle the form submission
@app.post
def send(msg:str, messages:list[str]=None):
    if not messages: messages = []
    messages.append(msg.rstrip())

    # Prepare the prompt for Ollama
    system_prompt = """You are a helpful assistant that invents weather for a specific location. 
                Use the tool WeatherComponent to generate a card for the given location."""
    
    # Call Ollama API
    response = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': msg},
        ],
        tools=tools_schema,
    )

    # Process the tool call response
    # Ollama returns a tool_calls list if the model decides to use a tool
    weather_card = P("Error: Could not generate weather.")
    
    if response.get('message') and response['message'].get('tool_calls'):
        tool_call = response['message']['tool_calls'][0]
        if tool_call['function']['name'] == 'WeatherComponent':
            # Parse arguments (Ollama returns a dict or JSON string depending on version)
            args = tool_call['function']['arguments']
            if isinstance(args, str):
                args = json.loads(args)
            
            # Call the local Python function to generate the FT Component
            weather_card = WeatherComponent(**args)

    return (ChatMessage(msg, True),    # The user's message
            ChatMessage(weather_card, False), # The assistant's response (rendered as a chat bubble containing the card)
            ChatInput()) # And clear the input field via an OOB swap

serve()
