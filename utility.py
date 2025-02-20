from itertools import permutations
from itertools import product

ws_lead_dict = {'Andrew': 3, 'Rissa': 3}
guitarist_dict = {'Andrew': 3, 'Rissa': 2}
pianist_dict = {'Eliza': 2}

# Generate all permutations of the unique candidates
def get_perms(the_set: set, the_len: int):
    res = []
    for perm in permutations(the_set, the_len):
        ws_lead, guitarist, pianist = perm

        # Enforce constraints:
        if ws_lead not in ws_lead_dict:  # ws_lead must be qualified
            continue
        if guitarist not in guitarist_dict:  # guitarist must be qualified
            continue
        if pianist not in pianist_dict:  # pianist must be qualified
            continue
        # Print valid assignment
        total_score = ws_lead_dict[ws_lead] + guitarist_dict[guitarist] + pianist_dict[pianist]
        res.append({'ws_lead': ws_lead, 'guitarist': guitarist, 'pianist': pianist, 'score': total_score})
    return res


def get_all_combinations(date_combinations):
    combinations = list(product(*date_combinations))
    # Check the total number of combinations
    return combinations