from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
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