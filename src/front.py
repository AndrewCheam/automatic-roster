import streamlit as st
import pandas as pd
from io import BytesIO

def process_csv(df):
    # Modify this function to process the CSV as needed
    df['Processed'] = 'Yes'  # Example modification
    return df

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

st.title("Church Duties Scheduling Tool")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded CSV:", df)
    
    processed_df = process_csv(df)
    st.write("### Processed CSV:", processed_df)
    
    csv_data = convert_df_to_csv(processed_df)
    st.download_button(label="Download Processed CSV", data=csv_data, file_name="processed_schedule.csv", mime="text/csv")
