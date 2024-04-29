#importing necessary libraries
import json
import anthropic
import requests
from bs4 import BeautifulSoup

#reading necessary files
with open("keys.txt", "r") as f:
    keys = f.read()
with open("specific_qna.json", "r") as f:
    s = json.load(f)

#generatimg user specific questions
#these questions are answered by hitting an API
#easily extended by updating the json file
specific = ""
for k,v in s.items():
    specific += f"User: {k} \n"
    specific += f"Type: SPECIFIC \n"
    specific += f"Answer: {v} \n"
print(specific)
'''
User: What is my account balance? 
Type: SPECIFIC 
Answer: account_balamce 
User: What is the Commission rate? 
Type: SPECIFIC 
Answer: commission_rate 
User: What is the yield on my account? 
Type: SPECIFIC 
Answer: yield 
User: What are the top 10 securities my fund has invested in? 
Type: SPECIFIC 
Answer: top_10_securities 
User: What sectors does the fund invested in? 
Type: SPECIFIC 
Answer: invested_securities 
User: What's the historical performance of my account? 
Type: SPECIFIC 
Answer: performance_history 
User: What's my contribution to my account so far this year? 
Type: SPECIFIC 
Answer: this_year_contribution 
User: How's my portfolio performed compared to market this week? 
Type: SPECIFIC 
Answer: portfolio_compared_market'''

#Web crawling for getting webpage content
def get_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

url = "https://retirementplans.vanguard.com/VGApp/pe/faces/web/help/ihelp/HelpCenter.xhtml"
generic_qa = get_website_content(url)
len(generic_qa.split())
#less than 5000 tokens
'''3768''




#Preparing the necessary prompt along with the generic and specific q&a

question = "Can you check my account balance?"

prompt = f""" Hi Claude, be an AI assistant in order to answer the user's account SPECIFIC questions give below
First classify the user question in to Type either "SPECIFIC" or "GENERIC" and answer differently for each Type

If the user asks "SPECIFIC" questions like below, respond with one word given in examples:
{specific}.

For User's "GENERIC" questions from the knowledge like below the Type for these would be "GENERIC":
{generic_qa}.

Give Weightage to "SPECIFIC" questions and try to answer it with a single word.

For "GENERIC" questions try to explain it in a concise human way

User: {question}
Type:
Answer:
"""


#Hitting the claude API with all necessary information
client = anthropic.Anthropic(

    api_key=keys,
)

message = client.messages.create(
    max_tokens=100,
    system = "Answer in less than 100 words or tokens",
    temperature = 0.5,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="claude-3-opus-20240229",
)
print(message.content[0].text)

'''
Type: SPECIFIC
Answer: account_balance
'''
#With this response we hit the correct API endpoint for the answer
