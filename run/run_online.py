#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

import gradio as gr
from model.freshprompt import llm
from model.freshprompt import demonstrations
from search import google

from dotenv import load_dotenv
import pdb


# @markdown ---
check_premise = True  # @param {type:"boolean"}
model_name = "gpt-4-1106-preview"
check_premise = True 

def configure():
    load_dotenv()

if __name__ == '__main__':
    configure()
        
    question = "Is it still a good idea to invest in NVIDIA now?"
    # answer = llm.call_freshprompt(
    #     model_name, 
    #     question, 
    #     check_premise=check_premise, 
    #     demo_search_data=demo_search_data
    # )

    def greet(name, intensity):
        return f"Hello {intensity} {name}!"

    demo = gr.Interface(
        fn=llm.call_freshprompt,
        inputs = [
            gr.Dropdown(
                value="gpt-4-1106-preview",
                label="LLM",
                choices=[
                    "gpt-4-1106-preview", 
                    "gpt-4", "gpt-4-32k", 
                    "gpt-3.5-turbo-1106", 
                    "gpt-3.5-turbo"
                ], 
                type="value"
            ),
            gr.Textbox(
                label="Question",
                value="Is it still a good idea to invest in NVIDIA now?"
            )
        ],
        outputs = [
            gr.Textbox(
                label="Answer",
                max_lines=20
            ),
            gr.Textbox(
                label="Evidences",
                max_lines=20
            ),
            gr.Textbox(
                label="Demonstrations",
                max_lines=20
            )
        ]
    )

    demo.launch(share=True)
    #demo.launch()


