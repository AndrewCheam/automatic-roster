from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any

class ScheduleModel:
    def __init__(self, **kwargs: Dict[str, Any]):
        """
        Initializes the ScheduleModel with the given parameters.

        :param kwargs: Dictionary containing various parameters required for scheduling.
        """
        # Base Requirements
        self.availability_df: pd.DataFrame = kwargs.get('availability_df')
        self.skills_df: pd.DataFrame = kwargs.get('skills_df')
        self.jobs_df: pd.DataFrame = kwargs.get('jobs_df')
        self.all_members: List[str] = kwargs.get('all_members')
        self.all_weeks: List[str] = kwargs.get('all_weeks')
        self.all_jobs: List[str] = kwargs.get('all_jobs')
        self.crucial_jobs: List[str] = kwargs.get('crucial_jobs')
        self.non_crucial_jobs: List[str] = kwargs.get('non_crucial_jobs')
        self.total_assignments_weight: int = kwargs.get('total_assignments_weight')
        self.assignment_deviation_weight: int = kwargs.get('assignment_deviation_weight')
        self.back_to_back_weight: int = kwargs.get('back_to_back_weight')
        
        # Custom Requirements
        self.max_roster_df: Optional[pd.DataFrame] = kwargs.get('max_roster_df')  # None if not present

        if isinstance(kwargs.get("proficiency_df"), pd.DataFrame): 
            self.proficiency_df: Optional[pd.DataFrame] = kwargs.get('proficiency_df') 
        else:
            # If proficiency_df not present, just take all proficiency as 1
            self.proficiency_df: Optional[pd.DataFrame] = pd.DataFrame(index=self.all_members, columns=self.all_jobs, data=1)
        self.proficiency_deviation_weight: int = kwargs.get('proficiency_deviation_weight')

        self.model: cp_model.CpModel = cp_model.CpModel()
        self.shifts: Dict[Tuple[str, str, str], cp_model.IntVar] = {}
        self.total_assignments: Dict[str, cp_model.IntVar] = {}
        self.back_to_back: Dict[str, cp_model.IntVar] = {}
        self.deviation: Dict[str, cp_model.IntVar] = {}
        self.squared_assignment_deviation: Dict[str, cp_model.IntVar] = {}
        self.total_proficiency_per_week: Dict[str, cp_model.IntVar] = {}

        # Set Constraints and Objectives
        self._create_variables()
        self._add_base_constraints()
        self._add_custom_constraints()
        self._set_objective()
    
    def _create_variables(self):
        """Creates the decision variables for the model."""
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
        
        self.squared_assignment_deviation = {
            m: self.model.NewIntVar(0, (len(self.all_weeks) * len(self.all_jobs)) ** 2, f"squared_assignment_deviation_{m}")
            for m in self.all_members
        }
        
        self.back_to_back = {
            m: self.model.NewIntVar(0, len(self.all_weeks) - 1, f"back_to_back_{m}")
            for m in self.all_members
        }
        self.total_proficiency_per_week = {
            w: self.model.NewIntVar(0, sum(self.proficiency_df.values.flatten()), f"total_proficiency_week_{w}")
            for w in self.all_weeks
        }

        self.min_proficiency_per_week = self.model.NewIntVar(0, np.sum(self.proficiency_df.values), "min_proficiency_per_week")


    def _add_base_constraints(self):
        """Adds the base constraints to the model."""
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
        
    def _add_custom_constraints(self):
        """Adds custom constraints to the model."""
        try:
            # Max Rostering Constraint
            if isinstance(self.max_roster_df, pd.DataFrame):
                for m in self.all_members:
                    max_shifts = self.max_roster_df.loc[m, "max_roster"]
                    if max_shifts != -1:  # Only enforce if there is a limit
                        self.model.Add(self.total_assignments[m] <= max_shifts)
        except:
            raise ValueError("One of the custom constraints didn't work...")

    def _set_objective(self):
        """Sets the objective function for the model."""
        # Penalise Deviation in Assignments
        avg_assignments = len(self.all_weeks) * len(self.all_jobs) // len(self.all_members)
        for m in self.all_members:
            self.model.Add(self.total_assignments[m] == sum(self.shifts[(m, w, j)] for w in self.all_weeks for j in self.all_jobs))
            # Get absolute deviation
            self.model.Add(self.deviation[m] >= self.total_assignments[m] - avg_assignments)
            self.model.Add(self.deviation[m] >= avg_assignments - self.total_assignments[m])
            # Square deviation to penalise outliers more
            self.model.AddMultiplicationEquality(self.squared_assignment_deviation[m], [self.deviation[m], self.deviation[m]])

        # Penalise Consecutive week assignments
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

        # Maximise the minimum proficiency across all weeks - naturally decreases deviation as well
        for w in self.all_weeks:
            self.model.Add(self.total_proficiency_per_week[w] == sum(
                self.shifts[(m, w, j)] * self.proficiency_df.loc[m, j]
                for m in self.all_members
                for j in self.all_jobs
            ))

        # Ensure min_proficiency_per_week is the minimum among all weeks
        self.model.AddMinEquality(self.min_proficiency_per_week, list(self.total_proficiency_per_week.values()))

        # Objective terms
        terms = []
        if self.total_assignments_weight != 0:
            terms.append(-sum(self.total_assignments[m] for m in self.all_members) * self.total_assignments_weight)
        if self.assignment_deviation_weight != 0:
            terms.append(sum(self.squared_assignment_deviation[m] for m in self.all_members) * self.assignment_deviation_weight)
        if self.back_to_back_weight != 0:
            terms.append(sum(self.back_to_back[m] for m in self.all_members) * self.back_to_back_weight)
        if self.proficiency_deviation_weight != 0 and self.proficiency_deviation_weight:
            terms.append(-self.min_proficiency_per_week * self.proficiency_deviation_weight)

        if terms:
            self.model.Minimize(sum(terms))

    def solve(self) -> Tuple[cp_model.CpSolver, int]:
        """
        Solves the scheduling model.

        :return: A tuple containing the solver instance and the status of the solution.
        """
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        return solver, status

    # def add_tri_roster_constraint(self):
    #     # No member should be rostered three weeks in a row
    #     for m in self.all_members:
    #         for w_idx in range(len(self.all_weeks) - 2):
    #             self.model.Add(
    #                 sum([self.shifts[(m, self.all_weeks[w_idx], j)] for j in self.all_jobs]) +
    #                 sum([self.shifts[(m, self.all_weeks[w_idx + 1], j)] for j in self.all_jobs]) +
    #                 sum([self.shifts[(m, self.all_weeks[w_idx + 2], j)] for j in self.all_jobs])
    #                 <= 2
    #             )