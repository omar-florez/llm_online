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