from langchain.chat_models import init_chat_model



llm = init_chat_model(
    model = 'gpt-4o-mini',
    base_url = 'https://api.chatanywhere.tech/v1',
    api_key = 'sk-Maf9m5KxsypZQ76kF2qQ6lsqLs3PL0cm2Bs3XeOD1yl6Lk86'
    
)