[![Stories in Ready](https://badge.waffle.io/my13/fa_mbd_2015b.png?label=ready&title=Ready)](https://waffle.io/my13/fa_mbd_2015b)
# Financial Analytics Software

The goal of this code is to provide analyst in the financial sector a python code to clean, manipulate and 
pick the best classification models according to its evaluation. 

## Overview

This project makes it easy to:
* Clean a dataset.
* Bin the data with a user interface or automatically. 
* Pick the best model for classification.

## Getting started

Download the python library from the pip repository:
  1.- Open your console
  2.- Input pip install fa_mbd_2015b (if you are on Windows environment)
  3.- Import the library on your code and start to use it. 
Download the last version of the code from the following link:
```shell
https://github.com/my13/fa_mbd_2015b
```
## Features

The code has two ways of interaction: The Automatic mode and the Human Assisted mode. The software follows the following structure:
* A1.py -> Automatic Data Cleaning code.
* A42.py -> Automated WoE Calculation, binning and Transformation with Automated Supervised Binning.
* A6.py -> Automated method comparison and choosing 
* H1.py -> Human Assisted Data Cleaning
* H3.py -> Human Assisted Binning

##### A1: Automatic Data Cleaning
Describes each column data type and automatically cleans the dataset by following the next strategies:
*In the case of strings that seem numeric, change them to numbers.
*In the case of different data types in a column, eliminate rows with minority data types.
*In the case of outliers, convert them in mean if float or median if interger.

##### A42: Automated WoE Calculation, binning and Transformation
This is a program that given a dataframe, does the following: obtains the name of the target variable, calculates the WoE for each value then the IV for each variable, bins the results into quintiles, creates a final dataframe with three columns: column name, IV, and binned value.

##### A6: Automated method comparison and choosing
Ask the user for the 'id' variable and the 'target' variable. Then, automatically calculates the accuracy of each model.

The models used in this programs are:
* AdaBoostClassifier 
* GradientBoostingClassifier 
* RandomForestClassifier 
* KNeighborsClassifier 
* SGDClassifier 

The output is a list of models with its accuracy.
The library used for these calculations is sklearn. (Go to [sklearn] (http://scikit-learn.org/stable/) documentation for more information)

##### H1: Human Assisted Data Cleaning
Find invalid values, display the number of rows and columns with Nans and ask the user to:
- Drop columns with more than 50% of Nans
- Drop rown with that contains Nans
- Choose an imputation strategy to fill the Nans. (Mean or median)

##### H3: Human Assisted Binning
The program lets the user decide the number of bins for each variable that should be binned, bin them and return the comparisons. It will not suggest the number of bins as this can be garnered from the automatic version of the program.

## Contributing

As we use this as our learning projects, I know this might not be the perfect approach
for all the projects out there. If you have any ideas, just
[open an issue][issues] and tell me what you think.

If you'd like to contribute, please fork the repository and make changes as
you'd like. Pull requests are warmly welcome.

## Licensing

This project is licensed under Unlicense license. This license does not require
you to take the license with you to your project.
