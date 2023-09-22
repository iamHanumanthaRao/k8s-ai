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
from PIL import Image

os.environ["OPENAI_API_KEY"]=openai_key

st.set_page_config(
   page_title="Alfred - AI",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

image = Image.open('Signeasy.png')
st.image("Signeasy.png", use_column_width=False)

genre = st.radio(
    "Tell AI the cluster you wanted",
    [":rainbow[Dev]", ":rainbow[QA]", ":rainbow[PP]", ":rainbow[DR]"]
    # captions = ["Laugh out loud.", "Get the popcorn.", "Never stop learning."]
    )

if genre == ':rainbow[Dev]':
    os.system('kubectl config use-context arn:aws:eks:us-east-1:751115992403:cluster/dev-01')
    st.write('You selected Dev Cluster.')
elif genre == ':rainbow[QA]':
    os.system('kubectl config use-context arn:aws:eks:us-east-1:751115992403:cluster/qa-01')
    st.write("You selected QA Cluster.")
elif genre == ':rainbow[DR]':
    os.system('kubectl config use-context arn:aws:eks:us-west-2:445819549122:cluster/DR-EKS')
    st.write("You selected DR Cluster.")
else:
    os.system('kubectl config use-context arn:aws:eks:us-east-1:751115992403:cluster/pp-01')
    st.write("You selected PP Cluster.")

st.title('Alfred - AI ')
input_text=st.text_input("What would you like to know today ?")

def writePods(info):
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template("index.html")
    lines = info
    headers = re.split(r'\s+', lines[0]) if lines else []
    rows = [re.split(r'\s+', line, maxsplit=len(headers)-1) for line in lines[1:]]
    rendered_html = template.render(headers=headers, rows=rows)
    components.v1.html(rendered_html, width=1200, height=600)    

def getInfo(cmd):
    try:
        result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pods_info = result.stdout.splitlines()
        writePods(pods_info)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        st.write("Please conect to the right VPN or check your Internet Connection")

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
        out = chain.run(input_text)
        print(out)
        st.write(out)
        getInfo(out)

gptInfo(input_text)