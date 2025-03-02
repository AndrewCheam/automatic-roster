import pandas as pd

def get_data():
    jobs_df = pd.read_csv('data/jobs.csv', index_col=0)
    availability_df = pd.read_csv('data/date_availability.csv', index_col=0).set_index('Names')
    skills_df = pd.read_csv('data/skills_mapping.csv', index_col=0).set_index('Names')

    # Test that availability_df and skills_df have the same names
    assert(set(availability_df.index) == set(skills_df.index)), "Date availability CSV needs to have same member names as Skills CSV!"
    # Test that jobs_df and skills_df have the same jobs
    assert(set(jobs_df['Jobs']) == set(skills_df.columns)), "Jobs CSV needs to have same jobs as Skills CSV!"

    all_members = list(availability_df.index)
    all_weeks = availability_df.columns
    all_jobs = list(jobs_df['Jobs'])
    crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 1])
    non_crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 0])

    return jobs_df, availability_df, skills_df, all_members, all_weeks, all_jobs, crucial_jobs, non_crucial_jobs
