import pandas as pd
import numpy as np
import ScheduleModel
import plotly.express as px
from ortools.sat.python import cp_model  # Assuming the solver is from OR-Tools

class SolutionViewer:
    def __init__(self, solver: cp_model.CpSolver, model: ScheduleModel):
        """
        Initializes the ScheduleGenerator with the solver and scheduling constraints.
        
        :param solver: The solver instance with the solved schedule.
        :param model: The scheduling model containing constraints and variables.
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
        
        self.schedule_df: pd.DataFrame | None = None

    def generate_schedule_df(self) -> pd.DataFrame:
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

    def analyze_schedule(self) -> tuple[px.bar, px.bar, px.scatter]:
        """Generates analytics based on the schedule."""
        if self.schedule_df is None:
            raise ValueError("Schedule not generated. Call generate_schedule_df() first.")

        # Total assignments per member
        assignments = {m: self.solver.Value(self.total_assignments[m]) for m in self.all_members}
        sorted_assignments = dict(sorted(assignments.items(), key=lambda item: item[1], reverse=True))

        # Bar chart for total assignments per member with different colors
        fig_assignments = px.bar(
            x=list(sorted_assignments.keys()),
            y=list(sorted_assignments.values()),
            color=list(sorted_assignments.values()),
            color_continuous_scale="blues"
        )
        fig_assignments.update_layout(
            # title="Total Assignments per Member",
            xaxis_title="Member",
            yaxis_title="Number of Assignments",
            plot_bgcolor="#f7faff",
            xaxis=dict(tickangle=-45)  # Tilt the x-axis labels
        )

        # Total proficiency per week
        proficiency = {w: self.solver.Value(self.total_proficiency_per_week[w]) for w in self.all_weeks}

        # Bar chart for total proficiency per week with consistent hue
        fig_proficiency = px.bar(
            x=list(proficiency.keys()),
            y=list(proficiency.values()),
            color=list(proficiency.values()),
            color_continuous_scale="tealrose"
        )
        fig_proficiency.update_layout(
            # title="Total Proficiency per Week",
            xaxis_title="Week",
            yaxis_title="Total Proficiency",
            plot_bgcolor="#f7faff",
            xaxis=dict(type='category')
        )

        # Back-to-back rosters heatmap
        back_to_back_data = {m: self.solver.Value(self.back_to_back[m]) for m in self.all_members}
        df_back_to_back = pd.DataFrame(list(back_to_back_data.items()), columns=["Member", "BackToBackCount"])

        # Group the data by back-to-back count and get the list of members
        back_to_back_summary = df_back_to_back.groupby('BackToBackCount').agg({
            'Member': lambda x: ', '.join(x)  # Combine names into a single string
        }).reset_index()

        # Count the number of people for each back-to-back count
        back_to_back_summary['NumPeople'] = back_to_back_summary['Member'].apply(lambda x: len(x.split(', ')))

        # Bubble chart
        fig_back_to_back = px.scatter(
            back_to_back_summary,
            x='BackToBackCount',
            y='NumPeople',
            size='NumPeople',
            color='BackToBackCount',
            hover_name='Member',  # Show names when hovering
            size_max=50,
            color_continuous_scale="Reds"
        )
        fig_back_to_back.update_layout(
            # title="Back-to-Back Rosters Bubble Chart",
            xaxis_title="Number of Back-to-Back Rosters",
            yaxis_title="Number of People",
            plot_bgcolor="#f7faff"
        )

        # Print additional metrics
        print(f"Squared Assignment Deviation: {sum(self.solver.Value(self.squared_assignment_deviation[m]) for m in self.all_members)}")
        print(f"Back to back rosters: {sum(self.solver.Value(self.back_to_back[m]) for m in self.all_members)}")
        print(f"Kena Back to Back Roster: {[m for m in self.all_members if self.solver.Value(self.back_to_back[m]) > 0]}")

        return fig_assignments, fig_proficiency, fig_back_to_back