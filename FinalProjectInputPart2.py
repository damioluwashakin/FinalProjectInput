# FinalProject.py

# Author: Damiola Oluwasakin

import csv
from datetime import datetime
from collections import defaultdict

#Student object
class Student:
    def __init__(self, student_id, last_name, first_name, major, gpa, graduation_date=None, disciplinary_action=False):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.gpa = gpa
        self.graduation_date = graduation_date
        self.disciplinary_action = disciplinary_action

#method for reading student data and populating student_data object
def read_student_data(file_path):
    student_data = defaultdict(list)
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            student_id, last_name, first_name, major, *disciplinary_action = row
            disciplinary_action = True if disciplinary_action[0] =='Y' else False
            student_data[major].append(Student(student_id, last_name, first_name, major, gpa_data[student_id], graduation_data[student_id], disciplinary_action))

    return student_data

#method for reading each student's gpa and maping theier id to their gpa for quick look up
def read_gpa_data(file_path):
    gpa_data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            student_id, gpa = row
            gpa_data[student_id] = float(gpa)

    return gpa_data

#method for mapping each student's id to their graduation date for quick loop up
def read_graduation_data(file_path):
    graduation_data = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            student_id, graduation_date = row
            graduation_data[student_id] = graduation_date

    return graduation_data

def interactive_query(student_data, gpa_data, graduation_data):
    while True:
        query = input("Enter major and GPA (e.g., 'Computer Science 3.5') or 'Q' to quit: ")
        if(query.lower() == 'q'):
            break
        major, gpa = None, None
        major_cnt, gpa_cnt = 0,0
        
        # looking for how many majors we find in the raw input string
        for _major in student_data:
            if query.lower().find(_major.lower()) != -1:
                major_cnt+=1
                major = _major
        
        query2 = query.split()
      
        # looking for how many gpa's we find in the raw input string
        for word in query2:
            if word.replace('.', '').replace(',', '').isdigit():
                gpa = float(word)
                gpa_cnt+=1
        
            
        #if parameters dont meet the constraints, user has to re query           
        if major is None or gpa is None or major_cnt > 1 or gpa_cnt > 1:
            print("Invalid input. Please enter a major and GPA.")
            continue

        if major not in student_data:
            print("No such major.")
            continue
        # Filter students
        matching_students = []
        similar_students = []
        closest_students = []
        for student in student_data[major]:
            graduation_date_parts = student.graduation_date.split('/') 
            year = int(graduation_date_parts[2])  
            month = int(graduation_date_parts[0])
            day = int(graduation_date_parts[1])  
        
            graduation_datetime = datetime(year, month, day)
            if graduation_datetime.date() > datetime.today().date() and not student.disciplinary_action:
                #for gpa's that match
                if(student.gpa == gpa):
                    matching_students.append(student)
                #if we dont have matching gpa's we look for similar gpa's
                elif abs(student.gpa - gpa) <= 0.25:
                    similar_students.append(student)
                #if !1 && !2 then we look for closest gpa's
                else:
                    closest_students.append(student)
            
        if matching_students:
            print("Your student(s):")
            for student in matching_students:
                print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
        elif similar_students:
            print("You may also consider:")
            for student in similar_students:
                print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")
        elif closest_students:
            print("No exact match found. Closest student:")
            for student in closest_students:
                print(f"ID: {student.student_id}, Name: {student.first_name} {student.last_name}, GPA: {student.gpa}")

        

if __name__ == "__main__":
    global gpa_data
    global graduation_data 
    global student_data
    
    gpa_data = read_gpa_data("GPAList.csv")
    graduation_data = read_graduation_data("GraduationDatesList.csv")
    student_data = read_student_data("StudentsMajorsList.csv")
    
    interactive_query(student_data, gpa_data, graduation_data)

