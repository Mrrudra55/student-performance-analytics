
# Student Performance Analytics System

## Project Overview

The Student Performance Analytics System is a Python-based
data analysis application that evaluates student marks,
attendance, grades, and academic performance.

It uses Python, NumPy, Pandas, and Streamlit to process
student records and present useful academic statistics
through an interactive dashboard.

## Objectives

- Calculate total and average marks.
- Assign grades based on defined rules.
- Identify passing and failing students.
- Analyze subject-wise performance.
- Compare department performance.
- Identify low attendance and academic support needs.
- Display results through an interactive dashboard.
- Export analyzed student data to CSV.

## Technologies Used

- Python
- NumPy
- Pandas
- Streamlit
- CSV
- Git and GitHub

## Project Structure

Student_Performance_Analytics/
├── main.py
├── functions.py
├── app.py
├── students.csv
├── requirements.txt
├── README.md
└── documentation/

## Installation

1. Install Python.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install the required libraries:

   pip install -r requirements.txt

## Running the Project

Run the command-line version:

   python main.py

Run the interactive dashboard:

   python -m streamlit run app.py

## Features

- Student marks analysis
- Automatic grade calculation
- Pass/fail identification
- Subject-wise statistics
- Department-wise analysis
- Attendance monitoring
- Academic support warnings
- Top performer identification
- CSV report downloads
- Interactive dashboard

## Dataset

The sample CSV file contains student identifiers,
names, departments, attendance percentages, and marks
in Python, Java, and Artificial Intelligence.

The included sample records are fictional.

## Project Rules

The example implementation assigns grades according
to average marks and identifies passing students
using a minimum mark requirement for every subject.

Attendance warnings use a configurable threshold.

These are project rules and should not be interpreted
as official college regulations.

## Author

Add your name, course, college, and academic year here.

## Future Improvements

- Additional subjects and configurable grading rules
- Improved data validation
- Student-wise detailed reports
- Additional visualizations
