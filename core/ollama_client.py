import ollama

def get_models():
    
    try:
        models = ollama.list()
    except Exception as e:
        print(f"Error occurred while fetching models: {e}")
        return []

    return [
        model.model
        for model in models.models
    ]

def chat( model, messages, options=None):

    return ollama.chat(
        model=model,
        messages=messages,
        options=options
            
    )
