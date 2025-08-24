from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

os.environ['LANGCHAIN_PROJECT'] = 'Sequential LLM App'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 2 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model1 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

model2 = ChatGroq(model="openai/gpt-oss-120b", temperature=0.5)

parser = StrOutputParser()

chain = prompt1 | model1 | parser | prompt2 | model2 | parser

config = {
    'run_name': 'sequential_chain_report_summary',
    'tag': ['sequential chain', 'report generation', 'summary generation', 'llm app'],
    'metadata': {
        'model1': 'llama-3.3-70b-versatile', 
        'model1_temp': '0.7',  
        'model2': 'openai/gpt-oss-120b', 
        'model2_temp': '0.5', 
        'parser': 'StrOutputParser'
    },
    'description': 'This chain generates a detailed report on a given topic and then summarizes it in 5 points.'
}

result = chain.invoke({'topic': 'Unemployment in karak, kpk, pakistan'}, config=config)

print(result)  