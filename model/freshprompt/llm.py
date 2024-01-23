from model.freshprompt.demonstrations import *
from model.freshprompt.format import *
from search.google import *

from openai import OpenAI
from dotenv import load_dotenv
import pdb

def configure():
  load_dotenv()
  
def create_client(openai_api_key):
  openai_client = OpenAI(api_key=openai_api_key)
  return openai_client

def call_llm_api(prompt, model, temperature, max_tokens, chat_completions=True):
  configure()
  openai_api_key = os.getenv('openai_api_key')
  openai_client = create_client(openai_api_key)

  # See https://platform.openai.com/docs/guides/gpt for details
  if chat_completions:
    # Chat completions API
    response = openai_client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
              "role": "system",
              "content": (
                "You are a helpful assistant. Answer as concisely as"
                f" possible. Knowledge cutoff: {current_date}."
                ),
            },
            {
              "role": "user", 
              "content": "What's today's date?"
            },
            {
              "role": "assistant",
              "content": f"Today is {current_date} in Pacific Standard Time.",
            },
            {
              "role": "user", 
              "content": prompt
            },
        ],
    )
    return response.choices[0].message.content
  else:
    # Completions API
    response = openai_client.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        prompt=prompt,
    )
    return response.choices[0].text

def call_freshprompt(model, question, check_premise=False, verbose=False, demo_search_data=None):
  if demo_search_data is None:
    demo_search_data = [call_search_engine(q) for q in demo_questions]

  temperature = 0.0
  max_tokens = 256
  chat_completions = True

  if model.startswith('gpt-4'):
    num_organic_results = 15
    #num_organic_results = 5
    num_related_questions = 3
    num_questions_and_answers = 3
    num_retrieved_evidences = 15
  else:
    num_organic_results = 15
    num_related_questions = 2
    num_questions_and_answers = 2
    num_retrieved_evidences = 5

  if verbose:
    demo_reasonings_and_answers = verbose_demo_reasonings_and_answers
  else:
    demo_reasonings_and_answers = concise_demo_reasonings_and_answers

  # Generate prompts for demo examples
  demo_prompts = []
  for q, s, ra in zip(
      demo_questions, demo_search_data, concise_demo_reasonings_and_answers
  ):
      demo_prompts.append(
      freshprompt_format(
          q,
          s,
          ra,
          num_organic_results,
          num_related_questions,
          num_questions_and_answers,
          num_retrieved_evidences,
      )
      )

  freshprompt_demo = ''.join(demo_prompts).strip()

  if check_premise:
    suffix = (
        "\nPlease check if the question contains a valid premise before"
        " answering.\nanswer: "
    )
  else:
    suffix = "\nanswer: "

  freshprompt_question = freshprompt_format(
      question,
      call_search_engine(question),
      suffix,
      num_organic_results,
      num_related_questions,
      num_questions_and_answers,
      num_retrieved_evidences,
  )

  #fresh_prompt = freshprompt_demo + freshprompt_question
  fresh_prompt = freshprompt_question
  answer = call_llm_api(
    fresh_prompt, model, temperature, max_tokens, chat_completions
  )
  #pdb.set_trace()
  return (answer, freshprompt_question, freshprompt_demo)