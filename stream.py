import os
import flask
from flask import Flask, render_template_string
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

st.title('Alfred Browser')
input_text=st.text_input("Search the topic u want")

def writePods(info):
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("index.html")
    pods = []
    for line in info:
        parts = re.split(r'\s+', line)
        print(parts)
        if len(parts) > 0:
            pods.append(parts)
    print(pods)
    rendered_html = template.render(pods=pods)
    components.v1.html(rendered_html, width=800, height=600)    

def getInfo(cmd):
    try:
        # Run the command and capture the output
        result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pods_info = result.stdout.splitlines()
        # os.system('echo "" >> index.html')
        # os.system('cp template.html index.html')
        # Print the command's output
        writePods(pods_info)
       
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

def gptInfo(input_text):
    first_input_prompt=PromptTemplate(
        input_variables=['command'],
        template="Command in k8s for {command}"
    )
    ## OPENAI LLMS
    llm=OpenAI(temperature=0.8)
    chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True)

    if input_text:
        out = chain.run(input_text)
        st.write(out)
        getInfo(out)



# Display HTML in Streamlit
    # components.v1.html(html_string, width=800, height=400)


gptInfo(input_text)
# viewhtml()