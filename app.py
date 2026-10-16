
import streamlit as st
import pandas as pd

from functions import (
    Calculate_total_marks,
    Calculate_average_marks,
    Assign_grades,
    Identify_pass_fail,
    Analyze_attendance,
    Identify_students_needing_support,
)

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.18);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎓 Student Performance Analytics")
st.caption(
    "Analyze academic performance, attendance, grades "
    "and student support requirements."
)

# ---------------- DATA LOADING ----------------

REQUIRED_COLUMNS = [
    "Student_ID", "Name", "Department", "Attendance",
    "Python", "Java", "AI"
]

uploaded_file = st.sidebar.file_uploader(
    "Upload student CSV",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        raw_data = pd.read_csv(uploaded_file)
    else:
        raw_data = pd.read_csv("students.csv")

    raw_data.columns = raw_data.columns.str.strip()

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in raw_data.columns
    ]

    if missing_columns:
        st.error(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    if raw_data.empty:
        st.error("The dataset contains no student records.")
        st.stop()

    # Validate and convert numerical columns
    numeric_columns = [
        "Student_ID", "Attendance", "Python", "Java", "AI"
    ]

    for col in numeric_columns:
        raw_data[col] = pd.to_numeric(
            raw_data[col], errors="raise"
        )

    if raw_data[REQUIRED_COLUMNS].isnull().any().any():
        st.error(
            "The dataset contains empty required fields. "
            "Please correct the CSV and upload it again."
        )
        st.stop()

    if not raw_data["Attendance"].between(0, 100).all():
        st.error("Attendance must be between 0 and 100.")
        st.stop()

    subjects = ["Python", "Java", "AI"]

    if not raw_data[subjects].apply(
        lambda column: column.between(0, 100).all()
    ).all():
        st.error("Subject marks must be between 0 and 100.")
        st.stop()

    # Use a copy so the original dataset remains unchanged
    students = raw_data.copy()

    students = Calculate_total_marks(students)
    students = Calculate_average_marks(students)
    students = Assign_grades(students)
    students = Identify_pass_fail(students)
    students = Analyze_attendance(students)
    students = Identify_students_needing_support(students)

except FileNotFoundError:
    st.error(
        "students.csv was not found. Put it in the "
        "same folder as app.py or upload a CSV."
    )
    st.stop()

except (ValueError, TypeError) as error:
    st.error(f"Please check the CSV data: {error}")
    st.stop()

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Dashboard Filters")

departments = sorted(
    students["Department"].astype(str).unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "Department",
    departments,
    default=departments
)

selected_status = st.sidebar.multiselect(
    "Pass / Fail",
    ["Pass", "Fail"],
    default=["Pass", "Fail"]
)

search_name = st.sidebar.text_input(
    "Search student by name or ID"
)

filtered = students[
    students["Department"].astype(str).isin(
        selected_departments
    )
    & students["Status"].isin(selected_status)
].copy()

if search_name.strip():
    query = search_name.strip().lower()

    filtered = filtered[
        filtered["Name"].astype(str).str.lower().str.contains(
            query, na=False
        )
        | filtered["Student_ID"].astype(str).str.contains(
            query, na=False
        )
    ]

# ---------------- OVERVIEW METRICS ----------------

st.subheader("Class Overview")

total_students = len(students)
passed = int((students["Status"] == "Pass").sum())
failed = int((students["Status"] == "Fail").sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric(
    "Class Average",
    f"{students['Average'].mean():.2f}%"
)
col3.metric("Passed", passed)
col4.metric("Failed", failed)

pass_percentage = (
    passed / total_students * 100 if total_students else 0
)

st.progress(
    int(round(pass_percentage)),
    text=f"Class pass rate: {pass_percentage:.1f}%"
)

# ---------------- CHARTS ----------------

st.subheader("Academic Performance")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Average Marks by Subject**")

    subject_averages = students[subjects].mean()

    st.bar_chart(subject_averages)

with chart_col2:
    st.markdown("**Grade Distribution**")

    grade_order = ["A+", "A", "B", "C", "D", "F"]

    grade_counts = (
        students["Grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
    )

    st.bar_chart(grade_counts)

st.subheader("Attendance Analysis")

attendance_col1, attendance_col2 = st.columns(2)

with attendance_col1:
    st.metric(
        "Average Attendance",
        f"{students['Attendance'].mean():.1f}%"
    )

with attendance_col2:
    low_attendance = int(
        (students["Attendance"] < 75).sum()
    )

    st.metric("Students Below 75% Attendance", low_attendance)

st.bar_chart(
    students.set_index("Name")["Attendance"],
    y_label="Attendance (%)"
)

# ---------------- DEPARTMENT ANALYSIS ----------------

st.subheader("Department-wise Analysis")

department_stats = students.groupby("Department").agg(
    Total_Students=("Student_ID", "count"),
    Average_Marks=("Average", "mean"),
    Average_Attendance=("Attendance", "mean")
).round(2)

st.dataframe(
    department_stats,
    width="stretch"
)

# ---------------- STUDENT EXPLORER ----------------

st.subheader("Student Explorer")

st.caption(
    f"Showing {len(filtered)} of {total_students} students "
    "based on your filters."
)

display_columns = [
    "Student_ID",
    "Name",
    "Department",
    "Attendance",
    "Python",
    "Java",
    "AI",
    "Total",
    "Average",
    "Grade",
    "Status",
    "Support_Status"
]

st.dataframe(
    filtered[display_columns].sort_values(
        "Average", ascending=False
    ),
    width="stretch",
    hide_index=True
)

# ---------------- TOP PERFORMERS ----------------

st.subheader("Top 5 Performers")

top_students = students.nlargest(5, "Average")

st.dataframe(
    top_students[
        ["Student_ID", "Name", "Department", "Average", "Grade"]
    ],
    width="stretch",
    hide_index=True
)

# ---------------- STUDENT SUPPORT ----------------

st.subheader("Students Requiring Support")

support_students = students[
    students["Support_Status"] != "No Immediate Warning"
]

if support_students.empty:
    st.success("No students currently meet the support-warning rules.")
else:
    st.dataframe(
        support_students[
            [
                "Student_ID", "Name", "Average",
                "Attendance", "Support_Status"
            ]
        ],
        width="stretch",
        hide_index=True
    )

# ---------------- DOWNLOAD REPORT ----------------

st.subheader("Download Reports")

report = students.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Complete Student Analysis CSV",
    data=report,
    file_name="student_analysis_report.csv",
    mime="text/csv"
)

filtered_report = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Student Report",
    data=filtered_report,
    file_name="filtered_student_report.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "Student Performance Analytics System | "
    "Built with Python, NumPy, Pandas and Streamlit"
)
