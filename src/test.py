def test_data(availability_df, skills_df, jobs_df):

    print('Testing Data Quality...')
    
    print("Checking if names appear in availability file")
    assert('Names' in availability_df.columns), "Ensure that Names column is in date_availability file"
    
    print("Checking if names appear in skills_mapping file")
    assert('Names' in skills_df.columns), "Ensure that Names column is in skills_mapping file"

    print("Checking for duplicate names in availability file")
    assert(len(availability_df['Names']) == len(set(availability_df['Names']))), "Ensure that Names are unique in date_availability file"

    print("Checking for duplicate names in skills_mapping file")
    assert(len(skills_df['Names']) == len(set(skills_df['Names']))), "Ensure that Names are unique in skills_mapping file"

    print("Checking that Names in both availability and skills_mapping files match")
    assert(set(availability_df['Names']) == set(skills_df['Names'])), "date_availability file needs to have same member names as skills_mapping file!"

    print("Checking that Jobs in job file exists")
    assert('Jobs' in jobs_df.columns and 'Crucial' in jobs_df.columns), "jobs file needs to have Jobs and Crucial columns!"
    
    print("Checking that Jobs in both jobs and skills_mapping files match")
    assert(set(jobs_df['Jobs']) == (set(skills_df.columns) - {'Names'})), "jobs file needs to have same jobs as skills_mapping file!"

    print('Data Quality is great!')