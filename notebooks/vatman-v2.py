
# coding: utf-8

# In[1]:


import pandas as pd
import json
import numpy as np
import re


# In[2]:


with open('/Users/Shared/vatman/items.json', 'r') as f:
    jsons = json.load(f)

df = pd.io.json.json_normalize(jsons)


# In[3]:


len(df.columns)


# In[5]:


df.head()


# In[6]:


len(df)


# In[7]:


df_recall = df.query("item_condition == 'nowy' and item_invoice == 'Wystawiam fakturę VAT-marża'")


# In[8]:


len(df_recall)


# In[9]:


with open('/Users/Shared/vatman/users.json', 'r') as f:
    user_jsons = json.load(f)

user_df = pd.io.json.json_normalize(user_jsons)


# In[10]:


len(user_df)


# In[11]:


user_recall = user_df[user_df.username.isin(df_recall.nick.unique()) & user_df.username.apply(lambda v: 'loombard' not in v.lower() and 'lombard' not in v.lower())]


# In[12]:


len(user_recall)


# In[13]:


user_recall


# In[14]:


user_recall['email_out'] = user_recall.apply(lambda r: ','.join(set(r['emails'] + r['more_emails'])), axis=1)
user_recall['phone_out'] = user_recall.apply(lambda r: ','.join(set(r['phone_numbers'] + r['more_phones'])), axis=1)
user_recall['nip_out'] = user_recall.nip.replace({None: '', np.NaN: ''})


# In[15]:


regexes = {
    'username': "^[a-zA-Z0-9._-]+$",
    'nip_out': "^\d{10}$",
    'email_out': "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
    'phone_out': "^\d{9,11}$"
}


# In[16]:


for k, v in regexes.items():
    user_recall[k] = user_recall[k].apply(lambda c: '' if re.match(v, c) is None else c)


# In[19]:


user_recall[['username', 'nip_out', 'email_out', 'phone_out']].to_csv('/Users/Shared/vatman/vatman_submission_2.csv', index=False, sep=';')


# In[18]:


re.match("^[a-zA-Z0-9._-]+$", "~~~dasdas") is None

