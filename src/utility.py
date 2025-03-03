from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
from test import test_data, test_solution

def get_df_from_app(date_availability_file, skills_mapping_file, jobs_file):
    if date_availability_file is None:
        raise ValueError("Error: Availability file not provided!")
    if skills_mapping_file is None:
        raise ValueError("Error: Skills file not provided!")
    if jobs_file is None:
        raise ValueError("Error: Jobs file not provided!")

    try:
        if date_availability_file.type == "text/csv":
            availability_df = pd.read_csv(date_availability_file, index_col=0)
        elif date_availability_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            availability_df = pd.read_excel(date_availability_file, index_col=0)

        if skills_mapping_file.type == "text/csv":
            skills_df = pd.read_csv(skills_mapping_file, index_col=0)
        elif skills_mapping_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            skills_df = pd.read_excel(skills_mapping_file, index_col=0)

        if jobs_file.type == "text/csv":
            jobs_df = pd.read_csv(jobs_file, index_col=0)
        elif jobs_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            jobs_df = pd.read_excel(jobs_file, index_col=0)
    
    except pd.errors.EmptyDataError:
        raise ValueError("Error: One or more files are empty!")
    except pd.errors.ParserError:
        raise ValueError("Error: files contain incorrect formatting!")

    test_data(availability_df, skills_df, jobs_df)
    return availability_df, skills_df, jobs_df

def get_data_from_csv(date_availability_file, skills_mapping_file, jobs_file):
    
    availability_df, skills_df, jobs_df = get_df_from_app(date_availability_file, skills_mapping_file, jobs_file)
    
    availability_df = availability_df.set_index("Names")
    skills_df = skills_df.set_index("Names")

    all_members = list(availability_df.index)
    all_weeks = availability_df.columns
    all_jobs = list(jobs_df['Jobs'])
    crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 1])
    non_crucial_jobs = list(jobs_df['Jobs'][jobs_df['Crucial'] == 0])

    # Store all data in a data dictionary

    data_dict = {}
    data_dict['jobs_df'] = jobs_df
    data_dict['availability_df'] = availability_df
    data_dict['skills_df'] = skills_df
    data_dict['all_members'] = all_members
    data_dict['all_weeks'] = all_weeks
    data_dict['all_jobs'] = all_jobs
    data_dict['crucial_jobs'] = crucial_jobs
    data_dict['non_crucial_jobs'] = non_crucial_jobs


    return data_dict



def get_model(jobs_df, availability_df, skills_df, all_members, all_weeks, all_jobs, crucial_jobs, non_crucial_jobs):
    """Creates and returns the CP-SAT model with constraints."""
    model = cp_model.CpModel()
    
    # Job assignment variables
    shifts = {
        (m, w, j): model.NewBoolVar(f"shift_m{m}_w{w}_j{j}")
        for m in all_members for w in all_weeks for j in all_jobs
    }
    
    # Each crucial job must be assigned exactly once per week
    for w in all_weeks:
        for j in crucial_jobs:
            model.AddExactlyOne(shifts[(m, w, j)] for m in all_members)

    # Each non-crucial job is assigned to at most one member per week
    for w in all_weeks:
        for j in non_crucial_jobs:
            model.AddAtMostOne(shifts[(m, w, j)] for m in all_members)

    # Each member does at most one job per week
    for m in all_members:
        for w in all_weeks:
            model.AddAtMostOne(shifts[(m, w, j)] for j in all_jobs)

    # Availability constraints
    for m in all_members:
        for w in all_weeks:
            if not availability_df.loc[m, w]: 
                for j in all_jobs:
                    model.Add(shifts[(m, w, j)] == 0)

    # Skill constraints
    for m in all_members:
        for j in all_jobs:
            if not skills_df.loc[m, j]: 
                for w in all_weeks:
                    model.Add(shifts[(m, w, j)] == 0)
    
    # Members cannot be rostered three weeks in a row
    for m in all_members:
        for w_idx in range(len(all_weeks) - 2):  
            for j in all_jobs:
                model.Add(
                    sum([shifts[(m, all_weeks[w_idx], j)] for j in all_jobs]) +
                    sum([shifts[(m, all_weeks[w_idx + 1], j)] for j in all_jobs]) +
                    sum([shifts[(m, all_weeks[w_idx + 2], j)] for j in all_jobs])
                    <= 2
                )

    # Fairness constraints (variance in job assignments)
    total_assignments = {
        m: model.NewIntVar(0, len(all_weeks) * len(all_jobs), f"total_assignments_{m}")
        for m in all_members
    }
    for m in all_members:
        model.Add(total_assignments[m] == sum(shifts[(m, w, j)] for w in all_weeks for j in all_jobs))

    # Compute mean assignments
    avg_assignments = len(all_weeks) * len(all_jobs) // len(all_members)

    # Deviation from mean
    deviation = {
        m: model.NewIntVar(0, len(all_weeks) * len(all_jobs), f"deviation_{m}")
        for m in all_members
    }
    for m in all_members:
        model.Add(deviation[m] >= total_assignments[m] - avg_assignments)
        model.Add(deviation[m] >= avg_assignments - total_assignments[m])

    # Squared deviation for variance minimization
    squared_deviation = {
        m: model.NewIntVar(0, (len(all_weeks) * len(all_jobs)) ** 2, f"squared_deviation_{m}")
        for m in all_members
    }
    for m in all_members:
        model.AddMultiplicationEquality(squared_deviation[m], [deviation[m], deviation[m]])

    # Minimize variance while ensuring maximum total assignments
    model.Minimize(-sum(total_assignments[m] for m in all_members) * 10 + sum(squared_deviation[m] for m in all_members))

    return model, shifts, total_assignments


def solve_model(model):
    """Solves the CP model and returns the solver with its status."""
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    solver.parameters.enumerate_all_solutions = False
    
    status = solver.Solve(model)
    return solver, status


def generate_schedule_df(solver, shifts, all_members, all_weeks, all_jobs):
    """Converts the solver result into a Pandas DataFrame."""
    solution_df = pd.DataFrame()
    solution_df["Job"] = all_jobs

    for w in all_weeks:
        week_list = []
        for j in all_jobs:
            job_filled = False
            for m in all_members:
                if solver.Value(shifts[(m, w, j)]):
                    week_list.append(m)
                    job_filled = True
                    break
            if not job_filled:
                week_list.append(np.nan)
        solution_df[f"{w}"] = week_list

    return solution_df


def schedule_jobs(date_availability_file, skills_mapping_file, jobs_file):
    """Main function: Loads data, creates model, solves, and returns schedule DataFrame."""
    # Load CSV files
    data_dict = get_data_from_csv(date_availability_file, skills_mapping_file, jobs_file)
    jobs_df = data_dict['jobs_df']
    availability_df = data_dict['availability_df']
    skills_df = data_dict['skills_df']
    all_members = data_dict['all_members']
    all_weeks = data_dict['all_weeks']
    all_jobs = data_dict['all_jobs']
    crucial_jobs = data_dict['crucial_jobs']
    non_crucial_jobs = data_dict['non_crucial_jobs']

    # Create the model
    model, shifts, total_assignments = get_model(jobs_df, availability_df, skills_df, all_members, all_weeks, all_jobs, crucial_jobs, non_crucial_jobs)

    # Solve the model
    solver, status = solve_model(model)

    if status == cp_model.OPTIMAL:
        print("\nOptimal solution found!")
        solution_df = generate_schedule_df(solver, shifts, all_members, all_weeks, all_jobs)
        test_solution(solution_df, availability_df, skills_df)

        # solution_df.to_csv('data/final_solution.csv')
        
        # Print total assignments per member
        print("\nTotal Assignments per Member:")
        for m in all_members:
            total = solver.Value(total_assignments[m])
            print(f"  - {m}: {total} jobs assigned")
        
        return solution_df
    
    elif status == cp_model.FEASIBLE:
        print("\nFeasible solution found, but not necessarily optimal.")
        return None
    else:
        print("\nNo solution found.")
        return None


### ONLY USED IN DEBUGGING FOR NOTEBOOKS###
class JobPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions, including total assignments per member."""

    def __init__(self, shifts, all_members, all_weeks, all_jobs, total_assignments, verbose = 0):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._all_members = all_members
        self._all_weeks = all_weeks
        self._all_jobs = all_jobs
        self._solution_count = 0
        self._total_assignments = total_assignments  # Track total assignments
        self._verbose = verbose

    def on_solution_callback(self):
        self._solution_count += 1
        if self._verbose == 1:
            print(f"\nSolution {self._solution_count}")

            # Print the solution table
            solution_df = pd.DataFrame()
            solution_df["Job"] = self._all_jobs
            for w in self._all_weeks:
                week_list = []
                for j in self._all_jobs:
                    job_filled = False
                    for m in self._all_members:
                        if self.Value(self._shifts[(m, w, j)]):
                            week_list.append(m)
                            job_filled = True
                    if not job_filled:
                        week_list.append(np.nan)
                solution_df[f"Week {w}"] = week_list
            display(solution_df)

            # Print total assignments per member
            print("\nTotal Assignments per Member:")
            for m in self._all_members:
                total = self.Value(self._total_assignments[m])  # Retrieve total assignments
                print(f"  - {m}: {total} jobs assigned")

    def solution_count(self):
        return self._solution_count
