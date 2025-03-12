import pandas as pd
import numpy as np
import ScheduleModel

class SolutionViewer:
    def __init__(self, solver, model:ScheduleModel):
        """
        Initializes the ScheduleGenerator with the solver and scheduling constraints.
        
        :param solver: The solver instance with the solved schedule.
        :param shifts: Dictionary of decision variables for shift assignments.
        :param total_assignments: Dictionary tracking total assignments per member.
        :param squared_assignment_deviation: Deviation metric for fairness evaluation.
        :param all_members: List of all members.
        :param all_weeks: List of all weeks.
        :param all_jobs: List of all jobs.
        """
        self.solver = solver
        self.shifts = model.shifts
        self.total_assignments = model.total_assignments
        self.squared_assignment_deviation = model.squared_assignment_deviation
        self.back_to_back = model.back_to_back
        self.all_members = model.all_members
        self.all_weeks = model.all_weeks
        self.all_jobs = model.all_jobs

        self.total_proficiency_per_week = model.total_proficiency_per_week
        
        self.schedule_df = None

    def generate_schedule_df(self):
        """Converts the solver result into a Pandas DataFrame."""
        solution_df = pd.DataFrame()
        solution_df["Job"] = self.all_jobs

        for w in self.all_weeks:
            week_list = []
            for j in self.all_jobs:
                job_filled = False
                for m in self.all_members:
                    if self.solver.Value(self.shifts[(m, w, j)]):
                        week_list.append(m)
                        job_filled = True
                        break
                if not job_filled:
                    week_list.append(np.nan)
            solution_df[f"{w}"] = week_list

        self.schedule_df = solution_df
        return solution_df

    def analyze_schedule(self):
        """Generates analytics based on the schedule."""
        if self.schedule_df is None:
            raise ValueError("Schedule not generated. Call generate_schedule_df() first.")
        
        # Print total assignments per member
        print("\nTotal Assignments per Member:")
        for m in self.all_members:
            total = self.solver.Value(self.total_assignments[m])
            print(f"  - {m}: {total} jobs assigned")
        
        print("\nTotal Proficiency per Week:")
        for w in self.all_weeks:
            total = self.solver.Value(self.total_proficiency_per_week[w])
            print(f"  - {w}: {total} proficiency")
        print(f"Squared Assignment Deviation: {sum(self.solver.Value(self.squared_assignment_deviation[m]) for m in self.all_members)}")
        print(f"Back to back rosters: {sum(self.solver.Value(self.back_to_back[m]) for m in self.all_members)}")
        print(f"Kena Back to Back Roster: {[m for m in self.all_members if self.solver.Value(self.back_to_back[m]) > 0]}")
        
        return None
