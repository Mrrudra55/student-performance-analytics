

from functions import (
    load_student_data,
    Calculate_total_marks,
    Calculate_average_marks,
    Assign_grades,
    Identify_pass_fail,
    Analyze_subjects,
    Get_top_students,
    Get_class_statistics,
    Analyze_attendance,
    Identify_students_needing_support,
    Department_analysis,
    Subject_pass_fail_analysis,
    Export_student_report
)


def main():
    # Load the dataset
    Students = load_student_data("students.csv")

    #process student performance
    Students = Calculate_total_marks(Students)
    Students = Calculate_average_marks(Students)
    Students = Assign_grades(Students)
    Students = Identify_pass_fail(Students)

    # Display individual students results
    print("\n=================STUDENTS PERFORMANCE==================")

    columns = [
        "Student_ID",
        "Name",
        "Total",
        "Average",
        "Grade",
        "Status"
    ]

    print(Students[columns].to_string(index=False))

    # Display class statistics
    print("\n=================CLASS STATISTICS==================")

    statistics = Get_class_statistics(Students)

    for name, value in statistics.items():
        print(f"{name}:{value}")


    #Display subject-wise analysis
    print("\n=================SUBJECT ANALYSIS==================")

    subject_average = Analyze_subjects(Students)
    
    for subject, average in subject_average.items():
          print(f"{subject} average:{average}")
  
    # Display top five students
    print("\n=================TOP 5 STUDENTS==================")

    top_students = Get_top_students(Students)

    print(
        top_students[["Student_ID", "Name", "Average", "Grade"]].to_string(index=False)
    )

    
    # Attendance and academic support analysis
    Students = Analyze_attendance(Students)
    Students = Identify_students_needing_support(Students)

    print("\n========== STUDENT SUPPORT REPORT ==========")

    print(
        Students[
            ["Name", "Average", "Attendance", "Support_Status"]
        ].to_string(index=False)
    )

    # Department-wise analysis
    print("\n========== DEPARTMENT ANALYSIS ==========")
    print(Department_analysis(Students))

    # Subject-wise pass/fail analysis
    print("\n========== SUBJECT PASS/FAIL ==========")

    subject_results = Subject_pass_fail_analysis(Students)

    for subject, results in subject_results.items():
        print(
            f"{subject}: Passed = {results['Passed']}, "
            f"Failed = {results['Failed']}"
        )

    # Export complete report
    Export_student_report(Students)



if __name__ == "__main__":
   main()

