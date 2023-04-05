# -*- coding: utf-8 -*-
"""GPT-3 Experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aDj6AnMxnVJf2RNhdd4yXCRGKQvDH8wl

The following code does not run. Will release complete code after results are published.

### Import Libraries
"""

# install openai
pip install --upgrade openai

import openai
import numpy as np
import builtins
import os
import pandas as pd

"""### GPT Settings"""

openai.api_key = "your_key"

"""### Link to Google Drive"""

from google.colab import drive

drive.mount('/content/gdrive')

"""### Load Task"""

data = pd.read_excel(r'/content/gdrive/My Drive/your_path/task.xlsx')

display(pd.DataFrame(data))

# Extract data
X = builtins.list(data['X']) # column 1 of task.xlsx
Y = builtins.list(data['Y']) # column 2 of task.xlsx
question = builtins.list(data['question']) # column 3 of task.xlsx

story = "story_prompt"

"""### Evaluate GPT-3 on Task"""

# Initialize storage for results
all_responses = pd.DataFrame() # N_prob x 5

temp = [0,0.25,0.5,0.75,1] # vary temperature [0,1]
col = ['1','2','3','4','5'] # one column per temperature
N_prob = len(question)
for t in range(len(temp)):
  responses = []
  for p in range(N_prob):
      # prompt
      prompt = story + X + Y + question # X, Y, and question varies for each problem
      # GPT-3 response
      response = openai.Completion.create(
      engine="text-davinci-003",
      prompt= prompt,
      temperature=temp[t],
      max_tokens=100,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0)
      responses.append(response['choices'][0]['text'])
  all_responses[col[t]] = responses # name each column in all_responses as col[t]

key = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # example key
gpt_t1 = [0, 1, 2, 4, 5, 6, 7, 9, 9, 10] # example gpt response at temp[1]

correct = [] 
for p in range(10):
  if key[p] == gpt_t1[p]: # need to store gpt responses in array
    correct.append(1)
  else:
    correct.append(0)
np.mean(correct) # percent correct

# save results to google drive
path = '/content/gdrive/My Drive/your_path/all_responses.csv'
with open(path, 'w', encoding = 'utf-8-sig') as f:
  all_responses.to_csv(f)