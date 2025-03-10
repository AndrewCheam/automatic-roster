import streamlit as st
import pandas as pd
from io import BytesIO
from JobScheduler import JobScheduler
import os

def process_csv(**kwargs):
    js = JobScheduler(**kwargs)
    df = js.schedule_jobs()
    return df

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output


def load_demo_file(file_path):
    try:
        return pd.read_csv(file_path, index_col=0)  # Or pd.read_excel(file_path) if it's an Excel file
    except FileNotFoundError:
        st.error(f"**Error:** {file_path} not found.")
        return None
    except Exception as e:
        st.error(f"**Error:** Something went wrong while reading {file_path}. Error details: {e}")
        return None

with st.sidebar:
    st.title("Guided Tour")
    st.markdown("""
    **Step 1**: Upload your **Availability File** (CSV/XLSX).
    **Step 2**: Upload the **Skills File** (CSV/XLSX).
    **Step 3**: Upload the **Jobs File** (CSV/XLSX).
    **Step 4**: (Optional) Select and upload additional constraint files.
    **Step 5**: Adjust the weights for scheduling constraints.
    **Step 6**: Click **Process Schedule** to generate the schedule.
    **Step 7**: Download the **processed schedule**.
    """)

st.title("Church Duties Scheduling Tool")

# Option to load demo files
use_demo_files = st.checkbox("Load Demo Files")

if use_demo_files:
    demo_availability_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/scheduler-backend/src/demo/demo_date_availability.csv')
    demo_skills_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/scheduler-backend/src/demo/demo_skills_mapping.csv')
    demo_jobs_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/scheduler-backend/src/demo/demo_jobs.csv')
    demo_max_roster_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/scheduler-backend/src/demo/demo_max_roster.csv')
    
    if demo_availability_file is not None and demo_skills_file is not None and demo_jobs_file is not None:
        st.write("###### Demo Availability File (Provide Names and their available dates)", demo_availability_file)
        st.write("###### Demo Skills File (Provide Names and the Jobs they can do)", demo_skills_file)
        st.write("###### Demo Jobs File (Provide Job Names and which must be filled for each date)", demo_jobs_file)
        st.write("###### Demo Max Roster File (Provide names and roster cap. -1 for no cap)", demo_max_roster_file)

date_availability_file = st.file_uploader("Upload Availability File", type=["csv", "xlsx", "xls"], key="availability")
skills_mapping_file = st.file_uploader("Upload Skills File", type=["csv", "xlsx", "xls"], key="skills")
jobs_file = st.file_uploader("Upload Jobs File", type=["csv", "xlsx", "xls"], key="jobs")

# Optional file uploaders
use_max_roster = st.checkbox("Include Max Roster File")
max_roster_file = None
if use_max_roster:
    max_roster_file = st.file_uploader("Upload Max Roster File", type=["csv", "xlsx", "xls"], key="max_roster")

# Sliders for weight adjustments
st.write("Adjust the priorities of that according to the needs of your roster. Higher number indicates higher priority.")
total_assignments_weight = st.slider("Prioritise number of roles filled (Non-crucial Jobs)", min_value=0, max_value=100, value=0)
deviation_weight = st.slider("Prioritise a balanced roster", min_value=0, max_value=100, value=0)
back_to_back_weight = st.slider("Prioritise less back to back roster for each member", min_value=0, max_value=100, value=0)

# Button to process the CSV
process_button = st.button("Generate Schedule", disabled=not (date_availability_file and skills_mapping_file and jobs_file and (not use_max_roster or max_roster_file)))

if process_button:
    try:

        processed_df = process_csv(
            date_availability_file=date_availability_file, 
            skills_mapping_file=skills_mapping_file, 
            jobs_file=jobs_file, 
            max_roster_file=max_roster_file,
            total_assignments_weight=total_assignments_weight,
            deviation_weight=deviation_weight,
            back_to_back_weight=back_to_back_weight
        )
        st.write("### Processed CSV:", processed_df)

        csv_data = convert_df_to_csv(processed_df)
        st.download_button(label="Download Processed CSV", data=csv_data, file_name="processed_schedule.csv", mime="text/csv")
    except Exception as e:
        st.error(f"**An error occurred while processing the files.**\n\nError details: {e}")
        st.write("Double check the input files and try again or contact the owner.")
        st.write("If the issue persists, please reach out to Andrew.")