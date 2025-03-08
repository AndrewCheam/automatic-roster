from ortools.sat.python import cp_model
import pandas as pd

class ScheduleModel:
    def __init__(self, **kwargs):
        
        # Base Requirements
        self.availability_df = kwargs['availability_df']
        self.skills_df = kwargs['skills_df']
        self.jobs_df = kwargs['jobs_df']
        self.all_members = kwargs['all_members']
        self.all_weeks = kwargs['all_weeks']
        self.all_jobs = kwargs['all_jobs']
        self.crucial_jobs = kwargs['crucial_jobs']
        self.non_crucial_jobs = kwargs['non_crucial_jobs']
        self.model = cp_model.CpModel()
        self.shifts = {}
        self.total_assignments = {}
        self.back_to_back = {}
        self.deviation = {}
        self.squared_deviation = {}
        
        # Custom Requirements
        self.max_roster_df = kwargs.get('max_roster_df') # None if not present

        # Set Constraints and Objectives
        self._create_variables()
        self._add_base_constraints()
        self._add_custom_constraints()
        self._set_objective()
    
    def _create_variables(self):
        self.shifts = {
            (m, w, j): self.model.NewBoolVar(f"shift_m{m}_w{w}_j{j}")
            for m in self.all_members for w in self.all_weeks for j in self.all_jobs
        }
        
        self.total_assignments = {
            m: self.model.NewIntVar(0, len(self.all_weeks) * len(self.all_jobs), f"total_assignments_{m}")
            for m in self.all_members
        }
        
        self.deviation = {
            m: self.model.NewIntVar(0, len(self.all_weeks) * len(self.all_jobs), f"deviation_{m}")
            for m in self.all_members
        }
        
        self.squared_deviation = {
            m: self.model.NewIntVar(0, (len(self.all_weeks) * len(self.all_jobs)) ** 2, f"squared_deviation_{m}")
            for m in self.all_members
        }
        
        self.back_to_back = {
            m: self.model.NewIntVar(0, len(self.all_weeks) - 1, f"back_to_back_{m}")
            for m in self.all_members
        }

    def _add_base_constraints(self):
        # Crucial job assignment constraints
        for w in self.all_weeks:
            for j in self.crucial_jobs:
                self.model.AddExactlyOne(self.shifts[(m, w, j)] for m in self.all_members)

        # Non-crucial job constraints
        for w in self.all_weeks:
            for j in self.non_crucial_jobs:
                self.model.AddAtMostOne(self.shifts[(m, w, j)] for m in self.all_members)

        # Each member does at most one job per week
        for m in self.all_members:
            for w in self.all_weeks:
                self.model.AddAtMostOne(self.shifts[(m, w, j)] for j in self.all_jobs)

        # Availability constraints
        for m in self.all_members:
            for w in self.all_weeks:
                if not self.availability_df.loc[m, w]: 
                    for j in self.all_jobs:
                        self.model.Add(self.shifts[(m, w, j)] == 0)

        # Skill constraints
        for m in self.all_members:
            for j in self.all_jobs:
                if not self.skills_df.loc[m, j]: 
                    for w in self.all_weeks:
                        self.model.Add(self.shifts[(m, w, j)] == 0)
        
        # No member should be rostered three weeks in a row
        for m in self.all_members:
            for w_idx in range(len(self.all_weeks) - 2):
                self.model.Add(
                    sum([self.shifts[(m, self.all_weeks[w_idx], j)] for j in self.all_jobs]) +
                    sum([self.shifts[(m, self.all_weeks[w_idx + 1], j)] for j in self.all_jobs]) +
                    sum([self.shifts[(m, self.all_weeks[w_idx + 2], j)] for j in self.all_jobs])
                    <= 2
                )

    def _add_custom_constraints(self):
        try:
            if isinstance(self.max_roster_df, pd.DataFrame):
                for m in self.all_members:
                    max_shifts = self.max_roster_df.loc[m, "max_roster"]
                    if max_shifts != -1:  # Only enforce if there is a limit
                        self.model.Add(self.total_assignments[m] <= max_shifts)
        except:
            raise ValueError("One of the custom constraint didnt work...")
    
    def _set_objective(self):
        avg_assignments = len(self.all_weeks) * len(self.all_jobs) // len(self.all_members)
        for m in self.all_members:
            self.model.Add(self.total_assignments[m] == sum(self.shifts[(m, w, j)] for w in self.all_weeks for j in self.all_jobs))
            self.model.Add(self.deviation[m] >= self.total_assignments[m] - avg_assignments)
            self.model.Add(self.deviation[m] >= avg_assignments - self.total_assignments[m])
            self.model.AddMultiplicationEquality(self.squared_deviation[m], [self.deviation[m], self.deviation[m]])

        # Consecutive week assignments
        for m in self.all_members:
            consecutive_assignments = []
            for w_idx in range(len(self.all_weeks) - 1):
                is_rostered_w = self.model.NewBoolVar(f"is_rostered_{m}_{self.all_weeks[w_idx]}")
                is_rostered_w_next = self.model.NewBoolVar(f"is_rostered_{m}_{self.all_weeks[w_idx + 1]}")
                self.model.Add(is_rostered_w == sum(self.shifts[(m, self.all_weeks[w_idx], j)] for j in self.all_jobs))
                self.model.Add(is_rostered_w_next == sum(self.shifts[(m, self.all_weeks[w_idx + 1], j)] for j in self.all_jobs))
                consecutive = self.model.NewBoolVar(f"consecutive_{m}_{self.all_weeks[w_idx]}")
                self.model.AddMultiplicationEquality(consecutive, [is_rostered_w, is_rostered_w_next])
                consecutive_assignments.append(consecutive)
            self.model.Add(self.back_to_back[m] == sum(consecutive_assignments))
        
        self.model.Minimize(-sum(self.total_assignments[m] for m in self.all_members) * 10 + 
                            sum(self.squared_deviation[m] for m in self.all_members) + 
                            sum(self.back_to_back[m] for m in self.all_members) * 10)
    
    def solve(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        return solver, status
