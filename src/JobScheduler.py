from ortools.sat.python import cp_model
from test import test_solution
import DataProcessor
from ScheduleModel import ScheduleModel
from SolutionViewer import SolutionViewer


class JobScheduler:
    """Encapsulates job scheduling logic."""
    
    def __init__(self, date_availability_file, skills_mapping_file, jobs_file):
        self.date_availability_file = date_availability_file
        self.skills_mapping_file = skills_mapping_file
        self.jobs_file = jobs_file

        self.data = DataProcessor.get_data(date_availability_file, skills_mapping_file, jobs_file)
        

    def schedule_jobs(self):
        """Solves the scheduling problem and returns a DataFrame of the schedule."""
        model = ScheduleModel(*self.data)
        solver, status = model.solve()
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("\nSolution found!")
            viewer = SolutionViewer(
                solver, model.shifts, model.total_assignments,
                model.squared_deviation, model.all_members,
                model.all_weeks, model.all_jobs
            )
            solution_df = viewer.generate_schedule_df()
            viewer.analyze_schedule()
            test_solution(solution_df, model.availability_df, model.skills_df)
            return solution_df
        
        raise ValueError("\nNo solution found.")
