import pandas as pd
from test import test_data


def load_data(**kwargs):

    data_dict = kwargs
    try:
        availability_df = load_and_set_index(kwargs.get('date_availability_file'), "Names", "Availability")
        skills_df = load_and_set_index(kwargs.get('skills_mapping_file'), "Names", "Skills")
        jobs_df = load_and_set_index(kwargs.get('jobs_file'), "Jobs", "Jobs")

        max_roster_df = load_and_set_index(kwargs.get('max_roster_file'), "Names", "Max Roster")
        proficiency_df = load_and_set_index(kwargs.get('proficiency_file'), "Names", "Proficiency")

    except ValueError as e:
        raise ValueError(str(e))  # Handle invalid file format or empty file errors

    except KeyError as e:
        raise ValueError(str(e))  # Handle missing column errors

    data_dict['availability_df'] = availability_df
    data_dict['skills_df'] = skills_df
    data_dict['jobs_df'] = jobs_df
    # Custom dfs
    data_dict['max_roster_df'] = max_roster_df
    data_dict['proficiency_df'] = proficiency_df
    filtered_data_dict = {k: v for k, v in data_dict.items() if v is not None}

    test_data(**filtered_data_dict)

    return filtered_data_dict

def get_data(**kwargs):
    data_dict = load_data(**kwargs)

    availability_df = data_dict['availability_df']
    skills_df = data_dict['skills_df']
    jobs_df = data_dict['jobs_df']
    
    data_dict['all_members'] = list(availability_df.index)
    data_dict['all_weeks'] = list(availability_df.columns)
    data_dict['all_jobs'] = list(jobs_df.index)  # Now jobs are the index
    data_dict['crucial_jobs'] = list(jobs_df.index[jobs_df['Crucial'] == 1])
    data_dict['non_crucial_jobs'] = list(jobs_df.index[jobs_df['Crucial'] == 0])
    data_dict['availability_df'] = availability_df
    data_dict['skills_df'] = skills_df
    data_dict['jobs_df'] = jobs_df

    print("Passing data dictionary into Schedule Model with key and value types: ")
    for k, v in data_dict.items():
        print(f'{k} : {type(v)}')
    
    return data_dict


def load_and_set_index(file, column_name, df_name="DataFrame"):
    """
    Loads a CSV or Excel file into a DataFrame, checks if the specified column exists,
    sets it as the index, and returns the modified DataFrame.

    Args:
        file (UploadedFile or None): The uploaded file object, or None.
        column_name (str): The column to set as the index.
        df_name (str): Optional name of the DataFrame for error messages.

    Returns:
        pd.DataFrame or None: The modified DataFrame with the column set as the index, or None if file is None.

    Raises:
        ValueError: If the file is empty or invalid.
        KeyError: If the column is missing in the DataFrame.
    """
    if file is None:
        return None

    try:
        # Load the file into a DataFrame
        if file.type == "text/csv":
            df = pd.read_csv(file, index_col=0)
        else:
            df = pd.read_excel(file, index_col=0)
        
        # Check if column name was already set as index
        if df.index.name == column_name:
            return df
        else:
            # Check if the column exists
            if column_name not in df.columns:
                raise KeyError(f"Error: '{column_name}' column is missing in {df_name}!")
            # Set the column as the index
            return df.set_index(column_name)

    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        raise ValueError(f"Error: Invalid file format or empty file for {df_name}!")




