from ortools.sat.python import cp_model
from test import test_solution, test_data
import DataProcessor
from ScheduleModel import ScheduleModel
from SolutionViewer import SolutionViewer

class JobScheduler:
    """Encapsulates job scheduling logic."""
    
    def __init__(self, **kwargs):
        """
        Initializes JobScheduler.

        Args:
            date_availability_file: Path to the availability file.
            skills_mapping_file: Path to the skills file.
            jobs_file: Path to the jobs file.
            model_kwargs: Additional keyword arguments for the model.
        """
        self.data = DataProcessor.get_data(**kwargs)

    def schedule_jobs(self):
        """Solves the scheduling problem and returns a DataFrame of the schedule."""
        model = ScheduleModel(**self.data)
        solver, status = model.solve()
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("\nSolution found!")
            viewer = SolutionViewer(
                solver, model
            )
            solution_df = viewer.generate_schedule_df()
            viewer.analyze_schedule()
            test_solution(solution_df, model.availability_df, model.skills_df)
            return solution_df
        
        raise ValueError("\nNo solution found.")
