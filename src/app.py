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


with st.sidebar:
    st.title("Guided Tour")
    st.markdown("""
    **Step 1**: Upload your **Availability File**  (CSV/XLSX).  
    **Step 2**: Upload the **Skills File**  (CSV/XLSX).  
    **Step 3**: Upload the **Jobs File** (CSV/XLSX).  
    **Step 4**: After uploading, you will be able to download the **processed schedule**.
    """)    


st.title("Church Duties Scheduling Tool")

date_availability_file = st.file_uploader("Upload Availability File", type=["csv", "xlsx", "xls"], key=1)
skills_mapping_file = st.file_uploader("Upload Skills File", type=["csv", "xlsx", "xls"], key=2)
jobs_file = st.file_uploader("Upload Jobs File", type=["csv", "xlsx", "xls"], key=3)

if not (date_availability_file and skills_mapping_file and jobs_file):
    st.info("Please upload the required files to start processing.")
    st.stop()

if date_availability_file and skills_mapping_file and jobs_file:
    # Read the files first
    # availability_df = pd.read_csv(date_availability_file)
    # skills_df = pd.read_csv(skills_mapping_file)
    # jobs_df = pd.read_csv(jobs_file)

    # Display them in Streamlit
    # st.write("### Availability CSV:", availability_df)
    # st.write("### Skills CSV:", skills_df)
    # st.write("### Jobs CSV:", jobs_df)
    try:
    # Reset file pointers before passing to another function, if not the file 'gets consumed the first time'
        date_availability_file.seek(0)
        skills_mapping_file.seek(0)
        jobs_file.seek(0)
        
        processed_df = process_csv(date_availability_file, skills_mapping_file, jobs_file)
        st.write("### Processed CSV:", processed_df)
        
        csv_data = convert_df_to_csv(processed_df)
        
        st.download_button(label="Download Processed CSV", data=csv_data, file_name="processed_schedule.csv", mime="text/csv")
    except Exception as e:
        # If an error occurs, display the error message and retry option
        st.error(f"**An error occurred while processing the files.**\n\nError details: {e}")
        st.write("Double check the input files and try again or contact the owner.")
        st.write("If the issue persists, please reach out to Andrew")
        # Display retry button


