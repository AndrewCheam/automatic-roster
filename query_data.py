import pandas as pd
from test import test_data

def get_data():
    
    jobs_df = pd.read_csv('data/jobs.csv', index_col=0)
    availability_df = pd.read_csv('data/date_availability.csv', index_col=0)
    skills_df = pd.read_csv('data/skills_mapping.csv', index_col=0)

    test_data(availability_df, skills_df, jobs_df)


    availability_df = availability_df.set_index("Names")
    skills_df = skills_df.set_index("Names")


    all_members = list(availability_df.index)
    all_weeks = availability_df.columns
    all_jobs = list(jobs_df['Jobs'])
    crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 1])
    non_crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 0])

    # Store all data in a data dictionary

    data_dict = {}
    data_dict['jobs_df'] = jobs_df
    data_dict['availability_df'] = availability_df
    data_dict['skills_df'] = skills_df
    data_dict['all_members'] = all_members
    data_dict['all_weeks'] = all_weeks
    data_dict['all_jobs'] = all_jobs
    data_dict['crucial_jobs'] = crucial_jobs
    data_dict['non_crucial_jobs'] = non_crucial_jobs


    return data_dict
