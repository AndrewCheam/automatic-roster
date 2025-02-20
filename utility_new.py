from itertools import permutations
from itertools import product
import numpy as np

ws_lead, support_singer, guitarist, pianist, drummer, bassist = None, None, None, None, None, None
ws_lead_dict = {'Andrew': 3, 'Yu Tang': 2, 'Wei En': 2, 'Noelle': 1, 'Chi Fei': 3, 'Chloe': 2, 'Rissa': 3, 'Gabriel': 2}
support_singer_dict = {'Jeremiah': 2, 'Zilu': 3}
guitarist_dict = {'Andrew': 3, 'Rissa': 2, 'Wei En': 2, 'Gabriel': 3, 'Jurina': 1}
pianist_dict = {'Wei En': 2, 'Ethan': 3, 'Jessica Wang': 2, 'Zilu': 1, 'Eliza': 3}
drummer_dict = {'Samuel': 3, 'Gabriel': 2, 'Jenson': 3, 'Mavis': 2}
bassist_dict = {'Chi Fei': 3, 'Wei En': 2}


all_dict = [ws_lead_dict, support_singer_dict, guitarist_dict, pianist_dict, drummer_dict, bassist_dict]
all_jobs = ['ws_lead', 'support_singer', 'guitarist', 'pianist', 'drummer', 'bassist']



# Generate all permutations of the unique candidates
def get_perms(the_set: set, the_len: int):
    res = []

    # Simulate no drummer
    filter_dict = [ws_lead_dict, support_singer_dict, guitarist_dict, pianist_dict, bassist_dict]
    filter_jobs = ['ws_lead', 'support_singer', 'guitarist', 'pianist', 'bassist']
    not_available_jobs = ['drummer']


    for perm in permutations(the_set, len(filter_dict)):
        valid_perm = True
        for i in range(len(filter_dict)):
            if perm[i] not in filter_dict[i]:
                valid_perm = False
                break
        if not valid_perm:
            continue

        total_score = sum([filter_dict[i][perm[i]] for i in range(len(filter_dict))])
        final_dict = { k:v for (k,v) in zip(filter_jobs, perm)}  
        for job in not_available_jobs:
            final_dict[job] = np.nan
        final_dict['total_score'] = total_score
        res.append(final_dict)
    return res


def get_all_combinations(date_combinations):
    combinations = list(product(*date_combinations))
    # Check the total number of combinations
    return combinations