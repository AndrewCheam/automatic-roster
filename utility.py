from itertools import permutations
from itertools import product

ws_lead, support_singer, guitarist, pianist, drummer, bassist = None, None, None, None, None, None
ws_lead_dict = {'Andrew': 3, 'Yu Tang': 2, 'Wei En': 2, 'Noelle': 1, 'Chi Fei': 3, 'Chloe': 2, 'Rissa': 3, 'Gabriel': 2}
support_singer_dict = {'Jeremiah': 2, 'Zilu': 3}
guitarist_dict = {'Andrew': 3, 'Rissa': 2, 'Wei En': 2, 'Gabriel': 3, 'Jurina': 1}
pianist_dict = {'Wei En': 2, 'Ethan': 3, 'Jessica Wang': 2, 'Zilu': 1, 'Eliza': 3}
drummer_dict = {'Samuel': 3, 'Gabriel': 2, 'Jenson': 3, 'Mavis': 2}
bassist_dict = {'Chi Fei': 3, 'Wei En': 2}


all_dict = [ws_lead_dict, support_singer_dict, guitarist_dict, pianist_dict, drummer_dict, bassist_dict]


# Generate all permutations of the unique candidates
def get_perms(the_set: set, the_len: int):
    res = []

    for perm in permutations(the_set, the_len):
        ws_lead, support_singer, guitarist, pianist, drummer, bassist = perm

        # Enforce constraints:
        if ws_lead not in ws_lead_dict:  # ws_lead must be qualified
            continue
        if support_singer not in support_singer_dict:  # support singer must be qualified
            continue
        if guitarist not in guitarist_dict:  # guitarist must be qualified
            continue
        if pianist not in pianist_dict:  # pianist must be qualified
            continue
        if drummer not in drummer_dict:  # drummer must be qualified
            continue
        if bassist not in bassist_dict:  # bassist must be qualified
            continue
        
        # Print valid assignment
        total_score = ws_lead_dict[ws_lead] + support_singer_dict[support_singer]+ guitarist_dict[guitarist] + pianist_dict[pianist] + drummer_dict[drummer] + bassist_dict[bassist]
        res.append({
            'ws_lead': ws_lead, 
            'support_singer': support_singer, 
            'guitarist': guitarist, 
            'pianist': pianist, 
            'drummer': drummer,
            'bassist': bassist,
            'score': total_score})
    return res


def get_all_combinations(date_combinations):
    combinations = list(product(*date_combinations))
    # Check the total number of combinations
    return combinations