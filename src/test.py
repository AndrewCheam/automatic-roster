def test_data(availability_df, skills_df, jobs_df):

    print('Testing Data Quality...')
    
    print("Checking if names appear in availability file")
    assert('Names' in availability_df.columns), "Ensure that Names column is in date_availability.csv"
    
    print("Checking if names appear in skills_mapping file")
    assert('Names' in skills_df.columns), "Ensure that Names column is in skills_mapping.csv"

    print("Checking that Names in both files match")
    assert(set(availability_df['Names']) == set(skills_df['Names'])), "Date availability CSV needs to have same member names as Skills CSV!"
    
    print("Checking that Jobs in both files match")
    assert(set(jobs_df['Jobs']) == (set(skills_df.columns) - {'Names'})), "Jobs CSV needs to have same jobs as Skills CSV!"

    print('Data Quality is great!')