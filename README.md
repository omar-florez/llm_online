# Description

LLMs learn static representation of knowledge in the weigths. Our experiments show that smaller models (7B) can compete with models of higher capacity such as ChatGPT and Llama 2 in perceived utility and F1 score if they access search engines to augment their reasoning power during in-context learning. 

# Steps to run

1. Create a file named `.env` in the root folder and define your API keys for [OpenAI](https://openai.com/pricing) and [SearchAPI](https://serpapi.com/).
- `touch .env`
```python
openai_api_key = ''
serpapi_api_key = ''
``` 
2. Run with: 
- `pip install -r requirements.txt`
- `python run/run_online.py`
