#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from scipy.special import comb
from itertools import combinations, permutations
import os


# In[7]:


#Read in data
df = pd.read_csv('transactions1.csv', header = None)
df2 =  pd.read_csv('transaction2.csv', header = None)
df3 =  pd.read_csv('transaction3.csv', header = None)
df4 =  pd.read_csv('transaction4.csv', header = None)
df5 =  pd.read_csv('transaction5.csv', header = None)


# In[13]:


def apyori(df, minimum_support, confidence):
    df_values = df.values.astype(str)
    index, counts = np.unique(df_values,return_counts=True)
    df_item = pd.DataFrame(zip(index, counts), columns = ['produto', 'frequencia'])
    df_item.drop(df_item[(df_item['produto'] == 'nan' )|(df_item['produto'] == 'None' )].index, inplace=True)
    df_item.sort_values(by='frequencia', ascending=False, inplace=True)
    df_item.reset_index(drop=True, inplace=True)
    df_item_frequent = df_item[df_item['frequencia']>= minimum_support*len(df)]
    df_itemset_frequencia = pd.DataFrame(columns=['itemset', 'frequencia'])
    for i in range(1, len(df_item_frequent)+1):
        comb = list(combinations(df_item_frequent['produto'].values, i) )
        for w in comb:
            count = 0
            for instancia in df_values:
                if all(elem in instancia  for elem in w):
                    count = count +1
            if count >= (minimum_support*len(df)/2):#tirar /2
                df_itemset_frequencia = df_itemset_frequencia.append({'itemset':w, 'frequencia':count}, ignore_index=True)
    df_itemset_frequencia.sort_values(by='frequencia', inplace=True, ascending=False)
    confiabilidade = pd.DataFrame(columns=['regras', 'frequencia', 'confiabilidade'])
    for w in df_itemset_frequencia['itemset'].values:
        w_p = list(permutations(w,len(w)))
        for j in w_p:
            #print (len(j[0]))

            p_uniao = []
            for i in range(len(j)):

                count = 0
                for instancia in df_values:
                    if all(elem in instancia  for elem in j[i:]):
                        count = count +1
                p_uniao.append(count/len(df))

            if len(j) != 1:
                a = p_uniao[-2]/p_uniao[-1]

                for i in range(len(p_uniao)-2):
                    a = p_uniao[-i-3]/a
                j = list(j)
                j.reverse()
                confiabilidade = confiabilidade.append({'regras':j, 'frequencia':p_uniao[0], 'confiabilidade':a}, ignore_index=True)
            else:
                confiabilidade = confiabilidade.append({'regras':j, 'frequencia':p_uniao[0], 'confiabilidade':p_uniao[0]}, ignore_index=True)
    confiabilidade.sort_values(by='frequencia', ascending=False)
    return confiabilidade[confiabilidade['confiabilidade']>=confidence]


# In[8]:


apyori(df).to_csv('Aprior_output.csv')


# In[17]:


support = input('Enter the minimum support value (0 to 1 values) for transaction 1: ')
confidence = input('Enter the minimum confidence value(0 to 1 values) for transaction 1: ')

support2 = input('Enter the minimum support value(0 to 1 values) for transaction 2: ')
confidence2 = input('Enter the minimum confidence value(0 to 1 values) for transaction 2: ')

support3 = input('Enter the minimum support value(0 to 1 values) for transaction 3: ')
confidence3 = input('Enter the minimum confidence value(0 to 1 values) for transaction 3: ')

support4 = input('Enter the minimum support value(0 to 1 values) for transaction 4: ')
confidence4 = input('Enter the minimum confidence value(0 to 1 values) for transaction 4: ')

support5 = input('Enter the minimum support value(0 to 1 values) for transaction 5: ')
confidence5 = input('Enter the minimum confidence value(0 to 1 values) for transaction 5: ')


# In[18]:


apyori(df, float(support), float(confidence)).to_csv('Apriori_output_transaction1.csv')
apyori(df2, float(support2), float(confidence2)).to_csv('Apriori_output_transaction2.csv')
apyori(df3, float(support3), float(confidence3)).to_csv('Apriori_output_transaction3.csv')
apyori(df4, float(support4), float(confidence4)).to_csv('Apriori_output_transaction4.csv')
apyori(df5, float(support5), float(confidence5)).to_csv('Apriori_output_transaction5.csv')
