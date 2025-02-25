from itertools import permutations
from itertools import product
import numpy as np
from collections import Counter

ws_lead_dict = {'Andrew': 3, 'Wei En': 4, 'Noelle': 3, 'Chloe': 1, 'Rissa': 3}
support_singer_dict = {'Jeremiah': 2, 'Zilu': 2, 'Chi Fei': 2}
guitarist_dict = {'Andrew': 4, 'Rissa': 3, 'Wei En': 4}
pianist_dict = {'Wei En': 5, 'Ethan': 3, 'Jessica Wang': 3, 'Zilu': 3, 'Eliza': 3}
drummer_dict = {'Gabriel': 5, 'Jenson': 3, 'Sarah': 2, 'Jurina': 3}
bassist_dict = {'Chi Fei': 2, 'Wei En': 5}

names = ['Andrew', 'Rissa', 'Eliza', 'Wei En', 'Gabriel', 'Chi Fei', 'Jeremiah', 'Zilu', 'Jessica Wang', 'Ethan', 'Jenson', 'Jurina', 'Chloe', 'Noelle', 'Sarah']
max_roster_dict = {name: 4 for name in names}
max_roster_dict['Gabriel'] = 1
max_roster_dict['Jurina'] = 1


# support_singer_dict = {}
bassist_dict = {}


job_dicts = [ws_lead_dict, support_singer_dict, guitarist_dict, pianist_dict, drummer_dict, bassist_dict]
jobs = ['ws_lead', 'support_singer', 'guitarist', 'pianist', 'drummer', 'bassist']


job_multipliers = [10, 2, 7, 7, 7, 4]
job_multipliers = [multiplier * 20 / sum(job_multipliers) for multiplier in job_multipliers] * 20 # times 20 since max score is 5




###################################################################################### MAIN FUNCTIONS WHICH ARE USED ##################################################################################
def get_perms_single_day(avail_people: set):
    res = []
    avail_dicts, avail_jobs, avail_job_multipliers, not_avail_jobs = get_avail_jobs(avail_people)
    for perm in permutations(avail_people, len(avail_dicts)):
        valid_perm = True
        for i, avail_dict in enumerate(avail_dicts):
            if perm[i] not in avail_dict:
                valid_perm = False
                break
        if not valid_perm:
            continue

        total_score = int(np.dot([job_dict[person] for job_dict, person in zip(avail_dicts, perm)], avail_job_multipliers))
        # total_score = sum([job_dict[person] for job_dict, person in zip(avail_dicts, perm)])
        # total_score = sum([avail_dicts[i][perm[i]] for i in range(len(avail_dicts))])
        final_dict = { k:v for (k,v) in zip(avail_jobs, perm)}  
        final_dict['people'] = set(final_dict.values())
        for job in not_avail_jobs:
            final_dict[job] = np.nan
        final_dict['total_score'] = total_score
        res.append(final_dict)
    return res
    
def get_comb_multi_day(date_combinations):
    combinations = list(product(*date_combinations))
    return combinations
           
def get_comb_multi_day_b2b_constraint(date_combinations):
   combinations = []
   dfs(date_combinations, 0, [], combinations)
   return combinations

def get_quarter_comb_with_score(combinations):
    combinations_with_score = [(comb, get_comb_score(comb)) for comb in combinations]
    combinations_with_score.sort(key=lambda x: x[1], reverse=True)
    return combinations_with_score

################################################################### HELPER FUNCTIONS FOR OTHER FUNCTIONS #####################################################################
def no_b2b_roster(roster1, roster2):
    return not bool(roster1['people'] & roster2['people']) # Returns True if there are no b2b rosters

def no_max_rostered(path, x):
    potential_path = path + [x]
    c = Counter([person for roster in potential_path for person in roster['people']])
    return all([True if c[k] <= max_roster_dict[k] else False for (k, v) in c.items()]) # Returns True if no person is max rostered
    
def dfs(lists, index, path, results):
   if index == len(lists):  # If we have selected from all lists
       results.append(path[:])  # Store a copy of the current selection
       return
   for x in lists[index]:  
       if index == 0 or (no_b2b_roster(x, path[-1]) and no_max_rostered(path, x)):  # Constraint: Ensure same people are not rostered twice in a row
           path.append(x)
           dfs(lists, index + 1, path, results)
           path.pop()  # Backtrack

def get_comb_score(quarter_comb):
    """
    Prioritise 
    1. Wide roster coverage
    2. Mean Value of scores
    3. Variances in day scores
    """
    all_set = set()
    for day_comb in quarter_comb:
        all_set = all_set | day_comb['people'] # Amount of people that are rostered
    mean_score = np.mean([day_comb['total_score'] for day_comb in quarter_comb]) # Mean Value
    neg_std_score = np.std([day_comb['total_score'] for day_comb in quarter_comb]) # Negative standard score
    return len(all_set), mean_score, neg_std_score
           
def get_avail_jobs(avail_people):
    avail_dicts = []
    avail_jobs = []
    avail_job_multipliers = []
    not_avail_jobs = []
    for i, job_dict in enumerate(job_dicts):
        if bool(set(job_dict.keys()) & avail_people):
            avail_dicts.append(job_dict)
            avail_jobs.append(jobs[i])
            avail_job_multipliers.append(job_multipliers[i])
        else:
            not_avail_jobs.append(jobs[i])
    return avail_dicts, avail_jobs, avail_job_multipliers, not_avail_jobs



    