# Automated Roster Scheduling

## Overview

This project implements an automated roster scheduling system using Google OR-Tools' Constraint Programming (CP-SAT) solver. The system assigns jobs to members while considering constraints such as availability, required skills, fairness, and workload balancing. This was super useful! https://xiang.es/posts/cp-sat/

## Features

### Basic Features:

- Ensures each crucial job is assigned exactly once per week.
- Assigns non-crucial jobs to at most one member per week.
- Ensures members are not over-assigned by limiting them to one job per week.
- Accounts for member availability and skill requirements.
- Prevents a member from being rostered three weeks in a row.
- Implements fairness by minimizing variance in job assignments.
- Outputs a CSV file containing the final schedule.

### Customizable Features:

- **Max Roster Constraint:** Allows specifying a maximum number of times certain members can be rostered.
- **Minimum Proficiency Constraint:** Ensures that the overall proficiency level for each week meets a required threshold.
- **Optimizing Variance in Proficiency:** Balances proficiency levels across weeks to maintain an even skill distribution.
- **Additional Custom Constraints:** Users can add new constraints based on specific scheduling requirements.

## Dependencies

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Data Requirements

The system requires the following CSV files:

1. `data/jobs.csv` - Contains job information and whether each job is crucial.
2. `data/date_availability.csv` - Specifies each member’s availability per week.
3. `data/skills_mapping.csv` - Maps members to the jobs they are qualified for.
4. `data/custom_constraints.csv` (optional) - Defines additional constraints such as max roster limits and minimum proficiency levels.

## Usage

### Step 1: Run the Streamlit Web App

Launch the interactive web app using Streamlit:

```bash
streamlit run app.py
```

This will open a web interface for uploading CSV files and generating a roster.

### Step 2: Upload Data

On the webpage, upload the required CSV files:

- Availability File
- Skills Mapping File
- Jobs File

The system will process the files and display the uploaded data before scheduling.

### Step 3: Generate and View the Roster

- The optimized schedule is displayed on the web interface.
- A downloadable CSV file (`final_solution.csv`) is generated for further use.

## Constraints Implemented

- **Job Assignment:** Every crucial job must be assigned exactly once per week.
- **Availability & Skills:** Members can only be assigned jobs they are available for and qualified to perform.
- **Workload Management:** A member cannot be assigned a job for three consecutive weeks.
- **Fairness:** The algorithm minimizes the variance in job assignments to ensure an equitable distribution.
- **Custom Constraints:** Additional constraints such as max roster limits and proficiency balancing can be incorporated using `data/custom_constraints.csv`.

## Output Example

After running the scheduler, a CSV file (`final_solution.csv`) is generated with the following structure:

| Job   | Week 1 | Week 2 | Week 3  | ... |
| ----- | ------ | ------ | ------- | --- |
| Job A | Alice  | Bob    | Charlie | ... |
| Job B | Bob    | Alice  | David   | ... |

Additionally, total assignments per member are displayed:

```bash
Total Assignments per Member:
  - Alice: 3 jobs assigned
  - Bob: 3 jobs assigned
  - Charlie: 2 jobs assigned
```

## Work in Progress

- **UI Enhancements:** Improving the web interface for better usability and visualization.
- **Analytics & Insights:** Adding features to analyze:
  - How many times each member is rostered.
  - Skill distribution among rostered members.
  - Fairness metrics and workload balancing.

## Troubleshooting

If the script does not find an optimal solution:

- Check if all crucial jobs can be assigned given the availability and skills constraints.
- Ensure that the `data/` CSV files are formatted correctly.
- Modify constraints if necessary to improve feasibility.

## License

This project is released under the MIT License.

## Author

Andrew Cheam
