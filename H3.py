
# coding: utf-8

# ### H.3) Human Assisted Binning 
# Program will let user decide number of bins for each variable that should be binned, bin them and return the comparisons. It will not suggest the number of bins as this can be garnered from the automatic version of the program
# 

# In[2]:

import pandas as pd
import numpy as np
df = pd.read_csv('https://dl.dropboxusercontent.com/u/28535341/dev.csv') 
df_clean = df # assign a clean dataframe if we need it later 


# In[3]:

# while loop to obtain user input on name of target variable
while True: 
    tv = input("Enter name of target variable (type e to exit):  ")   
    if tv in df.columns:
        print("Perfect! Thanks")
        break
    elif tv == 'e':
        break  


# In[4]:

while True: 
    id_var = input("Enter name of id variable (type e if none or to exit):  ")   
    if id_var in df.columns:
        print("Perfect! Thanks")  
        break
    elif id_var == 'e':   
        break  


# In[5]:

td1 = [id_var]
td  = [i for i in td1 if i != 'e']  
td = [x for x in td if len(x) > 0]  
df_drop = df.drop(td,axis=1)  


# In[22]:

def user_woe(df):  
    bin_list = []
    for var_name in df_drop: 
        if(len(df_drop[var_name].unique()) >= 24):  # more than 24 unique values to use binning 
            bin_list.append(var_name) 
    iv_list = [] 
    a= 0.01 
    for var_name in bin_list:  
        biv = pd.crosstab(df[var_name],df[tv])   
        WoE = np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)) #multiply by 1.0 to transform into float and add "a=0.01" to avoid division by zero.
        IV = sum(((1.0*biv[0]/sum(biv[0])+a) - (1.0*biv[1]/sum(biv[1])+a))*np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)))
        iv_list.append(IV)
    iv_list = iv_list
    test = pd.DataFrame({'Column Name' : bin_list,'IV' : iv_list}) 
    return(test.sort_values(by = 'IV', ascending = False)) 


# In[23]:

def user_bin(df):
    col_list = []  
    iv_list = []
    bins_list = []  
    iv_max = 0  
    a= 0.01  
    for var_name in df_drop: 
        if(len(df_drop[var_name].unique()) >= 24):  # more than 24 unique values to use binning (user cannot change) 
            col_list.append(var_name)  
    print("There are " + str(len(col_list)) + " columns that are elegible for binning")  
    print() 
    for var_name in col_list:  
        num = input('Please enter the number of bins you would like for varaible: ' + str(var_name) + 
                    ' (Min = '+ str(min(df[var_name])) + ', Max = '+ str(max(df[var_name])) + 
                    ', Std = ' + str(round(np.std(df[var_name]),2)) + ')')  
        bins = np.linspace(df[var_name].min(), df[var_name].max(), num) 
        groups = np.digitize(df[var_name], bins) 
        biv = pd.crosstab(groups,df[tv])   
        WoE = np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)) #multiply by 1.0 to transform into float and add "a=0.01" to avoid division by zero.
        IV = sum(((1.0*biv[0]/sum(biv[0])+a) - (1.0*biv[1]/sum(biv[1])+a))*np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)))    
        iv_list.append(IV) 
        bins_list.append(num)  
    test = pd.DataFrame({'Column Name' : col_list,'IV' : iv_list, 'Num_Bins' : bins_list})  
    return(test.sort_values(by = 'IV', ascending = False))


# In[24]:

# Function for determining value of IV    
def iv_binning(df2):   
    df2['Usefulness'] = ['Suspicous' if x > 0.5 else 'Strong' if x <= 0.5 and x > 0.3 else 'Medium'
                         if x <= 0.3 and x > 0.1 else 'Weak' if x <= 0.1 and x > 0.02 else
                         'Not Useful' for x in df2['IV']]  # Source for 'Usefullness Values' Siddiqi (2006) 
    return(df2)


# ### These are the two main functions for user assisted binning. The first allows the user to compare the IV for the selected number of bins with the scenario in which no binning was performed. The second transforms the orginal dataset according the number of bins selected for each variable.  

# In[25]:

def user_compare(df): # compares IV and Usefullness for binned and IV and Usefullness for unbinned varaibles  
    df1 = user_woe(df) 
    df_woe = iv_binning(df1) 
    df2 = user_bin(df)
    df_bin = iv_binning(df2) 
    common = df_bin.merge(df_woe,on=['Column Name'])  
    common.columns = ['Column Name', 'IV Bins', 'Num Bins', 'Usefulness IV', 'IV No Bins', 'Usefulness IV']
    return(common)


# In[ ]:

def user_transform(df): 
    common = user_compare(df) 
    bin_list = common['Num Bins']
    variable_list = common['Column Name']
    for idx,var_name in enumerate(variable_list):
        bins = np.linspace(df[var_name].min(), df[var_name].max(), bin_list[idx]) 
        df[var_name] = np.digitize(df[var_name], bins)  


# In[52]:



