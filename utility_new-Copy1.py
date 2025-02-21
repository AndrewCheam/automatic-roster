from itertools import permutations
from itertools import product
import numpy as np

ws_lead_dict = {'Andrew': 3, 'Yu Tang': 2, 'Wei En': 2, 'Noelle': 1, 'Chloe': 2, 'Rissa': 3}
support_singer_dict = {'Jeremiah': 2, 'Zilu': 3, 'Chi Fei': 3}
guitarist_dict = {'Andrew': 3, 'Rissa': 2, 'Wei En': 2, 'Gabriel': 3, 'Jurina': 1}
pianist_dict = {'Wei En': 2, 'Ethan': 3, 'Jessica Wang': 2, 'Zilu': 1, 'Eliza': 3}
drummer_dict = {'Samuel': 3, 'Gabriel': 2, 'Jenson': 3, 'Mavis': 2}
bassist_dict = {'Chi Fei': 3, 'Wei En': 2}

support_singer_dict = {}
bassist_dict = {}


job_dicts = [ws_lead_dict, support_singer_dict, guitarist_dict, pianist_dict, drummer_dict, bassist_dict]
jobs = ['ws_lead', 'support_singer', 'guitarist', 'pianist', 'drummer', 'bassist']



###################################################################################### MAIN FUNCTIONS WHICH ARE USED ##################################################################################
def get_perms_single_day(avail_people: set):
    res = []
    avail_dicts, avail_jobs, not_avail_jobs = get_avail_jobs(avail_people)
    for perm in permutations(avail_people, len(avail_dicts)):
        valid_perm = True
        for i, avail_dict in enumerate(avail_dicts):
            if perm[i] not in avail_dict:
                valid_perm = False
                break
        if not valid_perm:
            continue

        total_score = sum([avail_dicts[i][perm[i]] for i in range(len(avail_dicts))])
        final_dict = { k:v for (k,v) in zip(avail_jobs, perm)}  
        final_dict['people'] = set(final_dict.values())
        for job in not_avail_jobs:
            final_dict[job] = np.nan
        final_dict['total_score'] = total_score
        res.append(final_dict)
    return res
    

def get_comb_multi_day(date_combinations):
    combinations = list(product(*date_combinations))
    # Check the total number of combinations
    return combinations

           
def get_comb_multi_day_b2b_constraint(lists):
   results = []
   dfs(lists, 0, [], results)
   return results

################################################################### HELPER FUNCTIONS FOR OTHER FUNCTIONS #####################################################################
def b2b_roster(roster1, roster2):
    return bool(roster1['people'] & roster2['people'])
    
def dfs(lists, index, path, results):
   if index == len(lists):  # If we have selected from all lists
       results.append(path[:])  # Store a copy of the current selection
       return
   for x in lists[index]:  
       if index == 0 or not b2b_roster(x, path[-1]):  # Constraint: Ensure same people are not rostered twice in a row
           path.append(x)
           dfs(lists, index + 1, path, results)
           path.pop()  # Backtrack
           
def get_avail_jobs(avail_people):
    avail_dicts = []
    avail_jobs = []
    not_avail_jobs = []
    for i, job_dict in enumerate(job_dicts):
        if bool(set(job_dict.keys()) & avail_people):
            avail_dicts.append(job_dict)
            avail_jobs.append(jobs[i])
        else:
            not_avail_jobs.append(jobs[i])
    return avail_dicts, avail_jobs, not_avail_jobs
    