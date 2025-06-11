import streamlit as st
import pandas as pd
from io import BytesIO
from JobScheduler import JobScheduler
from streamlit.components.v1 import html
import time
import traceback


st.set_page_config(page_title="Church Duties Scheduler", layout="wide")

def switch(tab):
    return f"""
    var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
    var tab = tabGroup.getElementsByTagName("button")
    tab[{tab}].click()
    """

def process_csv(**kwargs):
    js = JobScheduler(**kwargs)
    df, fig_assignments, fig_proficiency, fig_back_to_back = js.schedule_jobs()
    return df, fig_assignments, fig_proficiency, fig_back_to_back

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def load_demo_file(file_path):
    try:
        return pd.read_csv(file_path, index_col=0)
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading file: {e}")
        return None

st.title("📅 Church Duties Scheduling Tool")

with st.sidebar:
    st.title("Guided Tour")
    st.markdown("""
    **Step 1**: Upload your **Availability File** (CSV/XLSX).\n
    **Step 2**: Upload the **Skills File** (CSV/XLSX).\n
    **Step 3**: Upload the **Jobs File** (CSV/XLSX).\n
    **Step 4**: (Optional) Select and upload additional constraint files.\n
    **Step 5**: Adjust the weights for scheduling constraints.\n
    **Step 6**: Click **Process Schedule** to generate the schedule.\n
    **Step 7**: Download the **processed schedule**.\n
    """)
    
    st.subheader("📂 Upload Required Files")
    date_availability_file = st.file_uploader("📅 Upload Availability File", type=["csv", "xlsx"])
    skills_mapping_file = st.file_uploader("🛠 Upload Skills File", type=["csv", "xlsx"])
    jobs_file = st.file_uploader("💼 Upload Jobs File", type=["csv", "xlsx"])
    
    use_max_roster = st.checkbox("Include Max Roster File")
    max_roster_file = st.file_uploader("🔢 Upload Max Roster File", type=["csv", "xlsx"]) if use_max_roster else None

    use_proficiency = st.checkbox("Include Proficiency File")
    proficiency_file = st.file_uploader("🔥 Upload Proficiency File", type=["csv", "xlsx"]) if use_proficiency else None
    
    st.subheader("⚙️ Adjust Scheduling Priorities")
    total_assignments_weight = st.slider("🔄 Ensure more jobs are assigned", 0, 100, 50, help="Higher values prioritize filling all jobs (When some are non-crucial).")
    assignment_deviation_weight = st.slider("⚖️ Balance workload among members", 0, 100, 50, help="Higher values distribute work evenly.")
    back_to_back_weight = st.slider("⏳ Reduce back-to-back assignments", 0, 100, 50, help="Higher values reduce consecutive duties.")
    proficiency_deviation_weight = st.slider("🔥 Balance and maximise proficiency across weeks", 0, 100, 50, help="Higher values distribute proficiency equally, and also increase proficiency across weeks.") if use_proficiency else None
    
    process_button = st.button("📝 Generate Schedule", disabled=not (date_availability_file and skills_mapping_file and jobs_file and (not use_max_roster or max_roster_file) and (not use_proficiency or proficiency_file)))

# Step Navigation
tab1, tab2 = st.tabs(["📊 View Demo Data", "📌 Generate Schedule"])

if process_button:
    html(f"<script>{switch(1)}</script>")

with tab1:
    st.subheader("🔍 Demo Data Files")
    st.markdown("""
    ℹ️ **About Demo Files:**
    - **Availability File:** Contains names and available dates.
    - **Skills File:** Lists members and the jobs they can do.
    - **Jobs File:** Defines crucial and non-crucial roles.
    - **Max Roster File (Optional):** Limits how many duties a person can take.
    - **Proficiency File (Optional):** Provides proficiency scores.
    """)
    
    demo_availability_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/main/src/demo/demo_date_availability.csv')
    demo_skills_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/main/src/demo/demo_skills_mapping.csv')
    demo_jobs_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/main/src/demo/demo_jobs.csv')
    demo_max_roster_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/main/src/demo/demo_max_roster.csv')
    demo_proficiency_file = load_demo_file('https://raw.githubusercontent.com/AndrewCheam/automatic-roster/refs/heads/main/src/demo/demo_proficiency.csv')
    
    if demo_availability_file is not None:
        st.write("### 📅 Availability File", demo_availability_file)
    if demo_skills_file is not None:
        st.write("### 🛠 Skills File", demo_skills_file)
    if demo_jobs_file is not None:
        st.write("### 💼 Jobs File", demo_jobs_file)
    if demo_max_roster_file is not None:
        st.write("### 🔢 Max Roster File", demo_max_roster_file)
    if demo_proficiency_file is not None:
        st.write("### 🔥 Proficiency File", demo_proficiency_file)

with tab2:
    st.subheader("🚀 Generate Schedule")
    if process_button:
        with st.spinner("⏳ Processing schedule..."):
            try:
                processed_df, fig_assignments, fig_proficiency, fig_back_to_back = process_csv(
                    date_availability_file=date_availability_file, 
                    skills_mapping_file=skills_mapping_file, 
                    jobs_file=jobs_file, 
                    max_roster_file=max_roster_file,
                    proficiency_file=proficiency_file,
                    total_assignments_weight=total_assignments_weight,
                    assignment_deviation_weight=assignment_deviation_weight,
                    back_to_back_weight=back_to_back_weight,
                    proficiency_deviation_weight=proficiency_deviation_weight
                )
                
                st.success("✅ Schedule generated successfully!")
                st.dataframe(processed_df, use_container_width=True)
                
                csv_data = convert_df_to_csv(processed_df)
                st.download_button("⬇️ Download Processed Schedule", data=csv_data, file_name="processed_schedule.csv", mime="text/csv")
                st.title("Schedule Analytics")

                st.subheader("Total Assignments per Member")
                st.plotly_chart(fig_assignments, use_container_width=True)

                st.subheader("Number of Back to Back rosters")
                st.plotly_chart(fig_back_to_back, use_container_width=True)


                st.subheader("Total Proficiency per Week")
                st.plotly_chart(fig_proficiency, use_container_width=True)
            except Exception as e:
                st.error(f"🚨 An error occurred: {e}")
                st.code(traceback.format_exc())  # Displays full traceback in a code block
            
    else:
        st.info("💡 No schedule generated yet. Upload files and click 'Generate Schedule' to start!")



