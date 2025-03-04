import pandas as pd
from test import test_data

def load_data(date_availability_file, skills_mapping_file, jobs_file):
    if not all([date_availability_file, skills_mapping_file, jobs_file]):
        raise ValueError("Error: One or more files not provided!")
    
    try:
        availability_df = pd.read_csv(date_availability_file, index_col=0) if date_availability_file.type == "text/csv" else pd.read_excel(date_availability_file, index_col=0)
        skills_df = pd.read_csv(skills_mapping_file, index_col=0) if skills_mapping_file.type == "text/csv" else pd.read_excel(skills_mapping_file, index_col=0)
        jobs_df = pd.read_csv(jobs_file, index_col=0) if jobs_file.type == "text/csv" else pd.read_excel(jobs_file, index_col=0)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        raise ValueError("Error: Invalid file format or empty files!")
    
    validate_data(availability_df, skills_df, jobs_df)
    
    return availability_df.set_index("Names"), skills_df.set_index("Names"), jobs_df

def validate_data(availability_df, skills_df, jobs_df):
    test_data(availability_df, skills_df, jobs_df)

def get_data(date_availability_file, skills_mapping_file, jobs_file):
    availability_df, skills_df, jobs_df = load_data(date_availability_file, skills_mapping_file, jobs_file)
    
    all_members = list(availability_df.index)
    all_weeks = availability_df.columns
    all_jobs = list(jobs_df['Jobs'])
    crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 1])
    non_crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 0])
    
    return availability_df, skills_df, jobs_df, all_members, all_weeks, all_jobs, crucial_jobs, non_crucial_jobs
