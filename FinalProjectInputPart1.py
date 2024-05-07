#Dami Oluwashakin
#1920721

import csv

# write function to read CSV files
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

# write function to write data to CSV files
def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# write function to sort by last name
def sort_by_last_name(record):
    return record[3]

# write function to sort by GPA
def sort_by_gpa(record):
    return float(record[4])

# write function to sort by graduation date
def sort_by_grad_date(record):
    return record[3]

# write function to process inventory reports
def process_reports(student_majors, gpa_data, grad_dates):
    full_roster = []
    major_students = {}
    scholarship_candidates = []
    disciplined_students = []

    # merge data from multiple files
    student_data = {}
    for row in student_majors:
        student_id, last_name, first_name, major, *disciplinary = row
        student_data[student_id] = [last_name, first_name, major, disciplinary]

    # process the GPA data
    for row in gpa_data:
        student_id, gpa = row
        if student_id in student_data:
            student_data[student_id].append(gpa)

    # process graduation dates
    for row in grad_dates:
        student_id, grad_date = row
        if student_id in student_data:
            student_data[student_id].append(grad_date)

    # generate full roster and majorwise lists
    for student_id, info in student_data.items():
        last_name, first_name, major, disciplinary, *rest = info
        gpa = rest[0] if rest else ''
        grad_date = rest[1] if len(rest) > 1 else ''
        full_roster.append([student_id, major, first_name, last_name, gpa, grad_date, disciplinary])

        if major not in major_students:
            major_students[major] = []
        major_students[major].append([student_id, last_name, first_name, grad_date, disciplinary])

        # then check for scholarship candidates
        if not disciplinary and gpa and float(gpa) > 3.8 and not grad_date:
            scholarship_candidates.append([student_id, last_name, first_name, major, gpa])

        # check for disciplined students
        if disciplinary:
            disciplined_students.append([student_id, last_name, first_name, grad_date])

    # sort the full roster by last name
    full_roster.sort(key=sort_by_last_name)

    # write full roster
    write_csv("FullRoster.csv", full_roster)

    # write major-wise lists
    for major, students in major_students.items():
        students.sort(key=lambda x: x[0])
        major_file_name = major.replace(" ", "") + "Students.csv"
        write_csv(major_file_name, students)

    # write scholarship candidates
    scholarship_candidates.sort(key=sort_by_gpa, reverse=True)
    write_csv("ScholarshipCandidates.csv", scholarship_candidates)

    # write disciplined students
    disciplined_students.sort(key=sort_by_grad_date)
    write_csv("DisciplinedStudents.csv", disciplined_students)

# read input files
student_majors = read_csv("StudentsMajorsList.csv")
gpa_data = read_csv("GPAList.csv")
grad_dates = read_csv("GraduationDatesList.csv")

# process reports
process_reports(student_majors, gpa_data, grad_dates)

print("Reports generated successfully.")
