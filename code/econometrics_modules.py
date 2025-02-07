import eurostat as eu
import os
import pandas as pd 
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def pull_data(code, name, folder = 'data', country = 'NL'):
    """
    Pull data from Eurostat, filter by country, and save to a CSV file.

    Parameters:
    code (str): The Eurostat dataset code.
    name (str): The name for the saved CSV file.
    folder (str): The folder where the CSV file will be saved.
    country (str): The country code to filter the data. Default is 'PL' (Poland).

    Returns:
    None
    """
    pars = eu.get_pars(code)
    par_values = eu.get_par_values(code , 'geo')
    dataset = eu.get_data_df(code, filter_pars= {'geo':'NL'})
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Define the full file path
    file_path = os.path.join(folder, name)
    
    # Save the dataset to a CSV file
    dataset.to_csv(file_path, index=False)
    



def is_year_month_format(date_str):
    """
    Check if a string is in the 'YYYY-MM' date format.

    Parameters:
    date_str (str): The string to check.

    Returns:
    bool: True if the string is in the 'YYYY-MM' format, False otherwise.
    """
    try:
        # Try to convert the column name to datetime with the specific format
        pd.to_datetime(date_str, format='%Y-%m')
        return True
    except ValueError:
        return False

def clean_dataframe(name, row_to_keep, file_name):
        """
    Clean the DataFrame by keeping specific rows and columns that match a certain date format,
    and then save the cleaned DataFrame to a CSV file.

    Parameters:
    name (pd.DataFrame): The DataFrame to clean.
    row_to_keep (int): The index of the row to keep.
    file_name (str): The name for the saved CSV file.

    Returns:
    None
    """
       
        # Keep only the specified row
        name = name.loc[[row_to_keep]]

        # Keep only columns with the 'YYYY-MM' date format
        columns_to_keep = [col for col in name.columns if is_year_month_format(col)]
        name = name[columns_to_keep]

        # Convert column names to datetime objects with the format '%Y-%m'
        name.columns = pd.to_datetime(name.columns, format = '%Y-%m')

        #Define the cutoff dates
        cutoff_date_begin = pd.Timestamp('2000-01')
        cutoff_date_end = pd.Timestamp('2024-11')

        # Use boolean indexing to filter out columns before the cutoff date
        columns_to_keep = [col for col in name.columns if  cutoff_date_end >= col >= cutoff_date_begin]
        name = name[columns_to_keep]

        # Save the dataset to the CSV file
        file_path = os.path.join('data', f'{file_name}.csv')
        name.to_csv(file_path, index=False)


def adf_test(series, signif=0.05, name=''):
    """Perform ADF test and print results"""
    r = adfuller(series, autolag='AIC')
    output = {'Test Statistic': r[0], 'p-value': r[1], '#Lags Used': r[2], 'Number of Observations Used': r[3]}
    for key, val in r[4].items():
        output[f'Critical Value ({key})'] = val
    print(f'ADF Test on "{name}"\n' + '-'*47)
    for key, val in output.items():
        print(f'{key} : {val}')
    print(f'Result: {"Series is Stationary" if r[1] <= signif else "Series is Non-Stationary"}')




