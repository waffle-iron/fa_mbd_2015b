import pandas as pd
import numpy
from sklearn.preprocessing import Imputer
import six
import ast
import time

df = pd.read_csv('https://dl.dropboxusercontent.com/u/28535341/dev.csv') 

def describe_df(dtf):
    int_type, str_type, float_type, undf  = {},{},{},{}
    print('Dataframe Shape:', df.shape)
    for cm in dtf.columns:
        int_type[cm] = [1 for x in list(dtf[cm]) if isinstance(x, six.integer_types) or isinstance(x, numpy.int64)]
        str_type[cm] = [1 for x in list(dtf[cm]) if isinstance(x, six.string_types)]
        float_type[cm] = [1 for x in list(dtf[cm]) if isinstance(x, float) or isinstance(x, numpy.float64)]
        undf[cm] = [1 for x in list(dtf[cm]) if x == None]
        print(cm, '--Row Type:',dtf[cm].dtype,':->', 
              'Integers:',round((sum(int_type[cm]) / len(dtf[cm])*100), 2),'%','--', 
              'Floats:',round((sum(float_type[cm]) / len(dtf[cm])*100), 2),'%','--',
              'Strings:',round((sum(str_type[cm]) / len(dtf[cm])*100), 2),'%','--', 
              'Empty Rows:',round(((dtf[cm].isnull().sum()+sum(undf[cm])) / len(dtf[cm])*100), 2),'%')

def try_numeric(dtf):
    int_type, str_type, float_type, undf  = {},{},{},{} 
    cvt = {}
    print('Trying to convert all values that appear to be numeric to numeric:') 
    for cm in dtf.columns:
        cvt[cm] = list(dtf[cm])
        for idx, row in enumerate(cvt[cm]):
            try:
                cvt[cm][idx] = ast.literal_eval(row.replace(',','.'))
            except:
                cvt[cm][idx] = row
            dtf[cm] = cvt[cm]
    for cm in dtf.columns:
            int_type[cm] = [1 for x in list(df[cm]) if isinstance(x, six.integer_types) or isinstance(x, numpy.int64)]
            str_type[cm] = [1 for x in list(df[cm]) if isinstance(x, six.string_types)]
            float_type[cm] = [1 for x in list(df[cm]) if isinstance(x, float) or isinstance(x, numpy.float64)]
            undf[cm] = [1 for x in list(df[cm]) if x == None]
            print(cm, '--Row Type:',df[cm].dtype,':->', 
                  'Integers:',round((sum(int_type[cm]) / len(dtf[cm])*100), 2),'%','--', 
                  'Floats:',round((sum(float_type[cm]) / len(dtf[cm])*100), 2),'%','--',
                  'Strings:',round((sum(str_type[cm]) / len(dtf[cm])*100), 2),'%','--', 
                  'Empty Rows:',round(((dtf[cm].isnull().sum()+sum(undf[cm])) / len(dtf[cm])*100), 2),'%')
    return(dtf)   

def eliminate_minority(dtf):
    print('1.Convert to most frequent Data Type')
    int_type, str_type, float_type, undf  = {},{},{},{} 
    for cm in dtf.columns:
        int_type[cm] = [1 for x in list(df[cm]) if isinstance(x, six.integer_types) or isinstance(x, numpy.int64)]
        str_type[cm] = [1 for x in list(df[cm]) if isinstance(x, six.string_types)]
        float_type[cm] = [1 for x in list(df[cm]) if isinstance(x, float) or isinstance(x, numpy.float64)]
        undf[cm] = [1 for x in list(df[cm]) if x == None]
        if(sum(int_type[cm]) > sum(str_type[cm]) and sum(int_type[cm]) > sum(float_type[cm])):
            df[cm] = [numpy.nan if isinstance(x, six.string_types) else x for x in list(df[cm])]
        elif(sum(str_type[cm]) > sum(int_type[cm]) and sum(str_type[cm]) > sum(float_type[cm])):
            df[cm] = [numpy.nan if isinstance(x, six.integer_types) or isinstance(x, numpy.int64) or
                      isinstance(x, float) or isinstance(x, numpy.float64)
                      else x for x in list(df[cm])]
        elif(sum(float_type[cm]) > sum(int_type[cm]) and sum(float_type[cm]) > sum(str_type[cm])):
            df[cm] = [numpy.nan if isinstance(x, six.string_types) else x for x in list(df[cm])]
    return(df.dtypes) 


def outlier(dtf):  # finds outliers within 3 standard deviations and converts to NaNs
    print("This code finds the outliers within 3 standard deviations and converts to NaNs") 
    b = len(dtf) 
    for var_name in dtf.columns: 
        dtf[var_name] = dtf[var_name][numpy.abs(dtf[var_name]-dtf[var_name].mean())<=(3*dtf[var_name].std())] 
        print(var_name,'->',len(list(dtf[var_name][numpy.abs(dtf[var_name]-dtf[var_name].mean())<=(3*dtf[var_name].std())])),
                         'not removed, original:', len(list(dtf[var_name]))) #keep only the ones that are within +3 to -3 standard deviations in the column 'Data'.
    print("Outliers removed") 
    return(dtf)

def impute(dtf): # imputes by mean if float, imputes by median if interger.         
    col_list = []
    nans_r = dtf.shape[0] - dtf.dropna().shape[0]
    perc_row = nans_r / len(dtf)  
    for var_name in dtf.columns:
        if dtf[var_name].isnull().sum() >= .50*len(dtf):   
            col_list.append(var_name)
    for var_name in dtf.columns: 
        if var_name in col_list:
            dtf = dtf.drop(col_list, axis = 1)
        elif perc_row < 0.02:
            dtf = dtf.dropna()
        elif dtf[var_name].dtype == "float64":
            dtf.fillna(dtf.mean()[var_name]) 
        else:
            dtf.fillna(dtf.median()[var_name]) 
    return(dtf)

describe_df(df)
nm_df = try_numeric(df)
em = eliminate_minority(nm_df)
ot = outlier(em)
impute(ot)