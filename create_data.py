import pandas as pd
import random

dates = ['d1', 'd2', 'd3', 'd4', 'd5']
input_col_names = ['name', 'd1', 'd2', 'd3', 'd4', 'd5']
names = ['Andrew', 'Rissa', 'Eliza', 'Wei En', 'Gabriel', 'Chi Fei', 'Jeremiah', 'Zilu', 'Jessica Wang', 'Ethan', 'Jenson', 'Jurina', 'Chloe', 'Noelle', 'Sarah']


def generate_fake_data(false_chance = 0.2):
    fake_data = [[name] + [True if random.random() > false_chance else False for _ in dates] for name in names]
    return pd.DataFrame(fake_data, columns=input_col_names)

if __name__ == '__main__':
    input_data = [
        ['Andrew', True, False, True, True, True],
        ['Rissa', True, True, False, True, False],
        ['Eliza', False, True, True, False, True],
        ['Wei En', False, True, True, True, False],
        ['Gabriel', True, False, True, False, True],
        ['Chi Fei', False, True, False, True, True],
        ['Jeremiah', True, False, True, True, False],
        ['Zilu', True, True, False, False, True],
        ['Jessica Wang', False, True, True, True, False],
        ['Ethan', True, False, False, True, True],
        ['Jenson', True, True, False, True, False],
        ['Jurina', False, True, True, False, True],
        ['Chloe', True, True, False, True, False],
        ['Noelle', False, False, True, True, True],
        ['Sarah', False, False, True, True, True]
    ]

    input_df = pd.DataFrame(input_data, columns=input_col_names)
    input_df.to_csv('taboo_dates.csv', index = False)
