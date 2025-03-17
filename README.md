# Automatic Roster

This project is designed to automate the scheduling of church duties. It uses various data inputs to generate an optimized schedule that balances workload, maximizes proficiency, and adheres to constraints such as availability and skill requirements.

## Try It Out

You can try out the application [here](https://auto-roster.streamlit.app/).

## Directory Structure

- `src/`
  - `app.py`: The main Streamlit application for interacting with the scheduling tool.
  - `DataProcessor.py`: Handles loading and processing of input data files.
  - `ScheduleModel.py`: Defines the scheduling model and constraints using OR-Tools.
  - `SolutionViewer.py`: Visualizes the generated schedule and provides analytics.
  - `test.py`: Contains functions for testing data quality and validating the generated schedule.
  - `demo/`: Contains demo CSV files for testing and demonstration purposes.

## Usage

### Step 1: Upload Required Files

1. **Availability File**: A CSV/XLSX file containing names and their availability dates.
2. **Skills File**: A CSV/XLSX file listing members and the jobs they can perform.
3. **Jobs File**: A CSV/XLSX file defining crucial and non-crucial roles.

### Step 2: Optional Constraint Files

1. **Max Roster File**: A CSV/XLSX file limiting the number of duties a person can take.
2. **Proficiency File**: A CSV/XLSX file providing proficiency scores for members.

### Step 3: Adjust Scheduling Priorities

Adjust the weights for various scheduling constraints using the sliders in the Streamlit sidebar.

### Step 4: Generate Schedule

Click the "Generate Schedule" button to process the schedule. The generated schedule and analytics will be displayed.

### Step 5: Download Schedule

Download the processed schedule as a CSV file.

## Demo Data

Demo data files are provided in the `demo/` directory for testing and demonstration purposes. These files include:

- `demo_date_availability.csv`
- `demo_skills_mapping.csv`
- `demo_jobs.csv`
- `demo_max_roster.csv`
- `demo_proficiency.csv`

## Testing

The `test.py` file contains functions to test data quality and validate the generated schedule. These tests ensure that the input data meets the required standards and that the generated schedule adheres to the defined constraints.

## Dependencies

- pandas
- numpy
- plotly
- ortools
- streamlit

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit application, use the following command:

```bash
streamlit run src/app.py
```

This will start the Streamlit server and open the application in your default web browser.

## License

This project is licensed under the MIT License.
