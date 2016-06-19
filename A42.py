print("A.4.2) Automated WoE Calculation, binning and Transformation with Automated Supervised Binning.")
print()
print("This is a program that given a dataframe, does the following: obtains the name of the target variable, calculates the WoE for each value then the IV for each variable, bins the results into quintiles, creates a final dataframe with three columns: column name, IV, and binned value.") 

# A.4.1 will recieve input from A.1. The result from A.1 should be a clean dataframe that is ready to run these calculations on. 
import pandas as pd
import numpy as np
df = pd.read_csv('https://dl.dropboxusercontent.com/u/28535341/dev.csv') 
df_clean = df # assign a clean dataframe if we need it later

# while loop to obtain user input on name of target variable
while True: 
    tv = input("Enter name of target variable (type e to exit):  ")   
    if tv in df.columns:
        print("Perfect! Thanks")
        break
    elif tv == 'e': 
        break  

while True: 
    id_var = input("Enter name of id variable (type e if none or to exit):  ")   
    if id_var in df.columns:
        print("Perfect! Thanks")  
        break
    elif id_var == 'e': 
        break

td1 = [tv,id_var]
td  = [i for i in td1 if i != 'e']   
td = [x for x in td if len(x) > 0]

# Function to calculate WOE and IV given a dataframe with no binning
def auto_woe(df): 
    iv_list = [] 
    a= 0.01
    df_drop_tar = df.drop(td, axis=1)  
    for var_name in df_drop_tar.columns: 
        biv = pd.crosstab(df[var_name],df[tv])   
        WoE = np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)) #multiply by 1.0 to transform into float and add "a=0.01" to avoid division by zero.
        IV = sum(((1.0*biv[0]/sum(biv[0])+a) - (1.0*biv[1]/sum(biv[1])+a))*np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)))
        iv_list.append(IV)
    iv_list = iv_list + [0] + [0] 
    col_list =list(df.columns)
    test = pd.DataFrame({'Column Name' : col_list,'IV' : iv_list})
    return(test.sort_values(by = 'IV', ascending = False))  

# Function for determing optimal number of bins (up to 20) for each variable with over 20 distint values using IV. 
# This is for running on samples only. 
def auto_bin(df):
    col_list = []
    loop_list = [i for i in range(1,21)]   
    iv_list = []
    bins_list = [] 
    iv_max = 0 
    a= 0.01
    df_drop_tar = df.drop(td, axis=1)  
    for var_name in df_drop_tar.columns:
        if(len(df[var_name].unique()) >= 24):  # more than 20 unique values to use binning   
            col_list.append(var_name)
    for var_name in col_list:  
        for i in loop_list: 
            bins = np.linspace(df[var_name].min(), df[var_name].max(), i)  
            groups = np.digitize(df[var_name], bins) 
            biv = pd.crosstab(groups,df[tv])   
            WoE = np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)) #multiply by 1.0 to transform into float and add "a=0.01" to avoid division by zero.
            IV = sum(((1.0*biv[0]/sum(biv[0])+a) - (1.0*biv[1]/sum(biv[1])+a))*np.log((1.0*biv[0]/sum(biv[0])+a) / (1.0*biv[1]/sum(biv[1])+a)))
            if IV > iv_max:
                iv_max = IV
                bin_f = len(bins)    
        iv_list.append(iv_max) 
        bins_list.append(bin_f)  
    #iv_list = iv_list + [0]
    #bins_list = bins_list + [0] 
    test = pd.DataFrame({'Column Name' : col_list,'IV' : iv_list, 'Num_Bins' : bins_list})  
    return(test.sort_values(by = 'IV', ascending = False))

# Function for determining value of IV    
def iv_binning(df2):   
    df2['Usefulness'] = ['Suspicous' if x > 0.5 else 'Strong' if x <= 0.5 and x > 0.3 else 'Medium'
                         if x <= 0.3 and x > 0.1 else 'Weak' if x <= 0.1 and x > 0.02 else
                         'Not Useful' for x in df2['IV']]  # Source for 'Usefullness Values' Siddiqi (2006)  
    return(df2)


print("These are secondary fuctions. The first gives  the sorted IV for all variables and their usefulness. The second gives the best number of bins and the associated IV and usefulness for the variables that can be binned.")  


def woe(df):     # gives IV for each variable and its usefullness   
    df1 = auto_woe(df) 
    df_woe = iv_binning(df1)
    return(df_woe)    

def bins(df):  # gives IV for binned variables and their usefullness
    df2 = auto_bin(df)
    df_bin = iv_binning(df2)
    return(df_bin)

print("These are the main functions. One to compare the automatically selected binning with the scenario in which no binning was performed and the other to transform the original dataset to a binned dataset using the automatically chosen binning.") 


def compare(df): # compares IV and Usefullness for binned and IV and Usefullness for unbinned varaibles  
    df1 = auto_woe(df) 
    df_woe = iv_binning(df1)  
    df2 = auto_bin(df)
    df_bin = iv_binning(df2) 
    common = df_bin.merge(df_woe,on=['Column Name'])  
    common.columns = ['Column Name', 'IV Bins', 'Num Bins', 'Usefulness IV', 'IV No Bins', 'Usefulness IV']
    return(common)   
 

def transform(df): # Bins dataset according to the best bins on the basis of an increase in IV
    common = compare(df) 
    bin_list = common['Num Bins']
    variable_list = common['Column Name']
    for idx,var_name in enumerate(variable_list): 
        bins = np.linspace(df[var_name].min(), df[var_name].max(), bin_list[idx])
        df[var_name] = np.digitize(df[var_name], bins) 



