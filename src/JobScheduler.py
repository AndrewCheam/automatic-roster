from ortools.sat.python import cp_model
from test import test_solution
import DataProcessor
from ScheduleModel import ScheduleModel
from SolutionViewer import SolutionViewer

class JobScheduler:
    """Encapsulates job scheduling logic."""
    
    def __init__(self, date_availability_file, skills_mapping_file, jobs_file, **optional_files):
        """
        Initializes JobScheduler.

        Args:
            date_availability_file: Path to the availability file.
            skills_mapping_file: Path to the skills file.
            jobs_file: Path to the jobs file.
            model_kwargs: Additional keyword arguments for the model.
        """
        self.base_data = DataProcessor.get_base_data(date_availability_file, skills_mapping_file, jobs_file)
        self.custom_data = DataProcessor.get_custom_data(**optional_files)

    def schedule_jobs(self):
        """Solves the scheduling problem and returns a DataFrame of the schedule."""
        model = ScheduleModel(*self.base_data, **self.custom_data)
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

# class JobScheduler:
#     """Encapsulates job scheduling logic."""
    
#     def __init__(self, date_availability_file, skills_mapping_file, jobs_file):

#         self.data = DataProcessor.get_data(date_availability_file, skills_mapping_file, jobs_file)
        
#         # data: availability_df, skills_df, jobs_df, all_members, all_weeks, all_jobs, crucial_jobs, non_crucial_jobs

#     def schedule_jobs(self):
#         """Solves the scheduling problem and returns a DataFrame of the schedule."""
#         model = ScheduleModel(*self.data)
#         solver, status = model.solve()
        
#         if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
#             print("\nSolution found!")
#             viewer = SolutionViewer(
#                 solver, model.shifts, model.total_assignments,
#                 model.squared_deviation, model.all_members,
#                 model.all_weeks, model.all_jobs
#             )
#             solution_df = viewer.generate_schedule_df()
#             viewer.analyze_schedule()
#             test_solution(solution_df, model.availability_df, model.skills_df)
#             return solution_df
        
#         raise ValueError("\nNo solution found.")