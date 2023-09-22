import os
import sys
from constants import openai_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain import LLMChain
from jinja2 import Environment, FileSystemLoader
import subprocess
import re
from streamlit import components

import streamlit as st

os.environ["OPENAI_API_KEY"]=openai_key

st.title('Alfred Browser 🔎')
input_text=st.text_input("Search the topic u want")

def writePods(info):
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("index.html")
    lines = info
    headers = re.split(r'\s+', lines[0]) if lines else []
    rows = [re.split(r'\s+', line, maxsplit=len(headers)-1) for line in lines[1:]]
    rendered_html = template.render(headers=headers, rows=rows)
    components.v1.html(rendered_html, width=800, height=600)    

def getInfo(cmd):
    try:
        result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pods_info = result.stdout.splitlines()
        writePods(pods_info)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

def gptInfo(input_text):
    keyWords = ["erase", "delete", "remove", "Delete", "DELETE"]
    first_input_prompt=PromptTemplate(
        input_variables=['command'],
        template="Command in k8s for {command}"
    )
    ## OPENAI LLMS
    llm=OpenAI(temperature=0.8)
    chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True)
    if input_text:
        for key in keyWords:
            if key in input_text:
                st.write("I don't have capabilites to perform this action")
                sys.exit()
            else:                    
                out = chain.run(input_text)
                st.write(out)
                getInfo(out)

gptInfo(input_text)