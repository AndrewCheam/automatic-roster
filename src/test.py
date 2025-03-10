

def test_data(**kwargs):

    require_names_check = ['availability_df', 'skills_df', 'max_roster_df']
    df_with_names = {k: v for k, v in kwargs.items() if k in require_names_check}

    print('Testing Data Quality...')
    check_names(**df_with_names)
    

    print("Checking that Jobs in job file exists")
    assert('Crucial' in kwargs['jobs_df'].columns), "jobs file needs to have Jobs and Crucial columns!"
    
    print("Checking that Jobs in both jobs and skills_mapping files match")
    assert(set(kwargs['jobs_df'].index) == (set(kwargs['skills_df'].columns))), "jobs file needs to have same jobs as skills_mapping file!"
    
    print('Data Quality is great!')
def check_names(**kwargs):
    print('Checking Names')
    
    for df_name, df in kwargs.items():
        print(f"Checking if duplicate names appear in {df_name} file")
        assert(len(df.index) == len(set(df.index))),f"Ensure that Names are unique in {df_name} file"

    prev_df = None  # Initialize previous value

    for idx, (df_name, df) in enumerate(kwargs.items()):
        # Check if current value has same names as previous value (but skip first iteration)
        if idx > 0:
            # Check whether they have the same names
            print(f"Checking that Names in both {df_name} and {prev_df_name} files match")
            assert(set(df.index) == set(prev_df.index)), f"{prev_df_name} file needs to have same member names as {df_name} file!"

        prev_df = df  # Update previous value for the next iteration
        prev_df_name = df_name

def test_solution(solution_df, availability_df, skills_df):
    # Test Cases based on user custom choices

    # Basic Solution Test Cases
    # test_n_roster_constraint(solution_df, max_b2b = 2)
    test_availability(solution_df, availability_df)
    test_skill_match(solution_df, skills_df)

# def test_n_roster_constraint(solution_df, max_b2b):
#     counter = {}
#     date_cols = solution_df.columns[1:]  # Exclude the job column
#     assert(max_b2b >= 1), "Max back to back roster has to be more than 0"
#     for idx, date in enumerate(date_cols):
#         if idx >= max_b2b:
#             # Check if any person is rostered more than twice in a row
#             assert all([(name not in counter) or (counter[name] < max_b2b) 
#                         for name in solution_df[date].dropna().values]), \
#                         f"Error with algorithm: {date} has a person rostered {max_b2b + 1} times in a row!"

#             # Remove column which was 2 steps ago from the counter
#             for name in solution_df[date_cols[idx - max_b2b]].dropna().values:
#                 if name in counter:
#                     counter[name] -= 1
#                     if counter[name] == 0:
#                         del counter[name]  # Clean up
#                 else:
#                     raise ValueError(f"Unexpected issue: {name} not found in counter while decrementing")
        
#         # Add new column into the counter
#         for name in solution_df[date].dropna().values:
#             counter[name] = counter.get(name, 0) + 1

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
