

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

def test_solution(solution_df, availability_df, skills_df):
    # Test Cases based on user custom choices

    # Basic Solution Test Cases
    test_tri_roster_constraint(solution_df)
    test_availability(solution_df, availability_df)
    test_skill_match(solution_df, skills_df)

def test_tri_roster_constraint(solution_df):
    counter = {}
    date_cols = solution_df.columns[1:]  # Exclude the job column

    for idx, date in enumerate(date_cols):
        if idx >= 2:
            # Check if any person is rostered more than twice in a row
            assert all([(name not in counter) or (counter[name] < 2) 
                        for name in solution_df[date].dropna().values]), \
                        f"Error with algorithm: {date} has a person rostered three times in a row!"

            # Remove column which was 2 steps ago from the counter
            for name in solution_df[date_cols[idx - 2]].dropna().values:
                if name in counter:
                    counter[name] -= 1
                    if counter[name] == 0:
                        del counter[name]  # Clean up
                else:
                    raise ValueError(f"Unexpected issue: {name} not found in counter while decrementing")
        
        # Add new column into the counter
        for name in solution_df[date].dropna().values:
            counter[name] = counter.get(name, 0) + 1

def test_availability(solution_df, availability_df):
    date_cols = solution_df.columns[1:]

    for date in date_cols:
        people = solution_df[date].dropna().values  # Get assigned people
        
        # Ensure all people exist in availability_df before checking availability
        missing_people = [name for name in people if name not in availability_df.index]
        assert not missing_people, f"Roster contains people not in availability data on {date}: {missing_people}"

        # Find people assigned on a "taboo" date
        unavailable_people = [name for name in people if not availability_df.loc[name, date]]
        assert not unavailable_people, f"Rostered on a taboo date ({date}): {unavailable_people}"

def test_skill_match(solution_df, skills_df):
    temp_df = solution_df.set_index('Job')  # Set 'Job' as index

    for job in temp_df.index:
        people = temp_df.loc[job].dropna().values  # Get assigned people

        # Check if they have the required skills
        invalid_people = [person for person in people if not skills_df.loc[person, job]]
        
        assert not invalid_people, f"People without required skills for {job}: {invalid_people}"
