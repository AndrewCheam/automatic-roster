def test_data(availability_df, skills_df, jobs_df):

    print('Testing Data Quality...')
    # Test that availability_df has name columns
    assert('Names' in availability_df.columns), "Ensure that Names column is in date_availability.csv"
    # Test that availability_df has name columns
    assert('Names' in skills_df.columns), "Ensure that Names column is in skills_mapping.csv"

    # Test that availability_df and skills_df have the same names
    assert(set(availability_df['Names']) == set(skills_df['Names'])), "Date availability CSV needs to have same member names as Skills CSV!"
    # Test that jobs_df and skills_df have the same jobs
    assert(set(jobs_df['Jobs']) == (set(skills_df.columns) - {'Names'})), "Jobs CSV needs to have same jobs as Skills CSV!"

    print('Data Quality is great!')