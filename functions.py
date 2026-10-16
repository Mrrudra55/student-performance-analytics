import numpy as np
import pandas as pd

def load_student_data(file_path):
    """Load student data from a CSV file."""
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df

def Calculate_total_marks(df):
    """ Calculate total marks for each student."""
    subjects = ["Python", "Java", "AI"]
    df["Total"] = df[subjects].sum(axis=1)
    return df

def Calculate_average_marks(df):
    """ Calculate average Marks for each students."""
    subjects = ["Python", "Java", "AI"]
    df["Average"] = df[subjects].mean(axis=1).round(2)
    return df

def Assign_grade(average):
    """ Asssign a grade based on the student's average."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

def Assign_grades(df):
    """ Assign grades to all Students."""
    df["Grade"] = df["Average"].apply(Assign_grade)
    return df

def Identify_pass_fail(df, passing_marks=40):
    """ A student passes only if every subject meets the passing mark."""
    subjects = ["Python", "Java", "AI"]

    df["Status"] = np.where(
        (df[subjects] >= passing_marks).all(axis=1),
        "Pass", "Fail"
    )

    return df

def Analyze_subjects(df):
    """ Calculate average marks for each subject"""
    subjects = ["Python", "Java", "AI"]

    return df[subjects].mean().round(2)

def Get_top_students(df, count=5):
    """ Return the top students based on average marks ."""
    return df.nlargest(count, "Average")

def Get_class_statistics(df):
    """Calculate overall class statistics."""

    return {
        "total Students": len(df),
        "Class Average": round(df["Average"].mean(), 2),
        "Highest Average": round(df["Average"].max(), 2),
        "Lowest Average": round(df["Average"].min(), 2),
        "Students Passed": int((df["Status"] == "Pass").sum()),
        "Students Failed": int((df["Status"] == "Fail").sum())
    }

def Analyze_attendance(df, minimum_attendance=75):
    """Identify students with low attendance."""
    df["Attendance_Status"] = np.where(
        df["Attendance"] < minimum_attendance,
        "Low Attendance",
        "Satisfactory"
    )
    return df


def Identify_students_needing_support(df):
    """Identify students with low marks or attendance."""
    conditions = [
        (df["Status"] == "Fail") & (df["Attendance"] < 75),
        (df["Status"] == "Fail"),
        (df["Attendance"] < 75)
    ]

    choices = [
        "High Priority",
        "Academic Support",
        "Attendance Support"
    ]

    df["Support_Status"] = np.select(
        conditions,
        choices,
        default="No Immediate Warning"
    )

    return df


def Department_analysis(df):
    """Calculate performance for each department."""
    return df.groupby("Department").agg(
        Total_Students=("Student_ID", "count"),
        Average_Marks=("Average", "mean"),
        Average_Attendance=("Attendance", "mean")
    ).round(2)


def Subject_pass_fail_analysis(df):
    """Count passing and failing students in each subject."""
    subjects = ["Python", "Java", "AI"]
    results = {}

    for subject in subjects:
        passed = int((df[subject] >= 40).sum())
        failed = int((df[subject] < 40).sum())

        results[subject] = {
            "Passed": passed,
            "Failed": failed
        }

    return results


def Export_student_report(df, filename="student_analysis_report.csv"):
    """Save analyzed student data to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"\nReport exported successfully: {filename}")
