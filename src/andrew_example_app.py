import streamlit as st
import pandas as pd
from io import BytesIO
from utility import schedule_jobs

def process_csv(date_availability_file, skills_mapping_file, jobs_file):
    # Modify this function to process the CSV as needed
    df = schedule_jobs(date_availability_file, skills_mapping_file, jobs_file)
    return df

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

st.title("Church Duties Scheduling Tool")

date_availability_file = st.file_uploader("Upload Availability File", type=["csv", "xlsx", "xls"], key=1)
skills_mapping_file = st.file_uploader("Upload Skills File", type=["csv", "xlsx", "xls"], key=2)
jobs_file = st.file_uploader("Upload Jobs File", type=["csv", "xlsx", "xls"], key=3)


if date_availability_file and skills_mapping_file and jobs_file:
    # Read the files first
    # availability_df = pd.read_csv(date_availability_file)
    # skills_df = pd.read_csv(skills_mapping_file)
    # jobs_df = pd.read_csv(jobs_file)

    # Display them in Streamlit
    # st.write("### Availability CSV:", availability_df)
    # st.write("### Skills CSV:", skills_df)
    # st.write("### Jobs CSV:", jobs_df)

    # Reset file pointers before passing to another function, if not the file 'gets consumed the first time'
    date_availability_file.seek(0)
    skills_mapping_file.seek(0)
    jobs_file.seek(0)
    
    processed_df = process_csv(date_availability_file, skills_mapping_file, jobs_file)
    st.write("### Processed CSV:", processed_df)
    
    csv_data = convert_df_to_csv(processed_df)
    st.download_button(label="Download Processed CSV", data=csv_data, file_name="processed_schedule.csv", mime="text/csv")
