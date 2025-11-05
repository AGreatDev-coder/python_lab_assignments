def calculate_average(marks_dict):
    len_dict = len(marks_dict)
    if len_dict == 0:
        return 0
    else:
        total_marks = sum(marks_dict.values())
        average = total_marks / len_dict
        return average
    
def calculate_median(marks_dict):
    marks_list = sorted(marks_dict.values())
    len_list = len(marks_list)
    if len_list == 0:
        return 0
    else:
        mid = len_list // 2
        if len_list % 2 == 0:
            median = (marks_list[mid - 1] + marks_list[mid]) / 2
        else:
            median = marks_list[mid]
        return median
    
def find_max_score(marks_dict):
    for student, score in marks_dict.items():
        if score == max(marks_dict.values()):
            return student, score
        
def find_min_score(marks_dict):
    for student, score in marks_dict.items():
        if score == min(marks_dict.values()):
            return student, score
        
def print_gradebook(marks_dict):
    print("Gradebook:")
    grade_distribution={}
    for key,value in marks_dict.items():
        if value >= 90:
            grade="a"
            grade_distribution[key]=grade
        elif value >= 80:
            grade="b"
            grade_distribution[key]=grade
        elif value >= 70:
            grade="c"
            grade_distribution[key]=grade
        elif value >= 60:
            grade="d"
            grade_distribution[key]=grade
        else:
            grade="f"
            grade_distribution[key]=grade
    return grade_distribution

def grade_distribution(marks_dict):
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for score in marks_dict.values():
        if score >= 90:
            distribution['A'] += 1
        elif score >= 80:
            distribution['B'] += 1
        elif score >= 70:
            distribution['C'] += 1
        elif score >= 60:
            distribution['D'] += 1
        else:
            distribution['F'] += 1
    return distribution

def pass_or_fail(marks_dict):
    results = {}
    passed = []
    failed = []
    for student, score in marks_dict.items():
        if score >= 40:
            results[student] = 'Pass'
            passed.append(student)
        else:
            results[student] = 'Fail'
            failed.append(student)
    return passed,len(passed), failed, len(failed),results

def print_results_table(marks_dict, grade_dist):

    # Set fixed column widths for consistent spacing
    NAME_WIDTH = 15
    MARKS_WIDTH = 8
    GRADE_WIDTH = 8
    SEPARATOR = "-" * (NAME_WIDTH + MARKS_WIDTH + GRADE_WIDTH + 6) # +6 for the spaces
    name=[]

    # Header Row (Left-align Name, Right-align Marks and Grade)
    header = f"{'Name':<{NAME_WIDTH}} | {'Marks':>{MARKS_WIDTH}} | {'Grade':>{GRADE_WIDTH}}"
    print(header)
    print(SEPARATOR)
    l=len(marks_dict)

    for i in marks_dict.items(): 
        name=list(marks_dict.keys())

    for j in range (len(name)):
        print(f"{name[j]:<{NAME_WIDTH}} | {marks_dict[name[j]]:>{MARKS_WIDTH}} | {grade_dist[name[j]]:>{GRADE_WIDTH}}")
    print()
        
#__main__

print("Gradebook Management System")

marks_dict = {}
n=int(input("Enter the number of students: "))
for i in range(n):
    student_name = input("Enter the student's name: ")
    student_marks = int(input("Enter the student's marks: "))
    marks_dict[student_name] = student_marks

average_marks = calculate_average(marks_dict)
print(f"Average Marks: {average_marks:.2f}")

median_marks = calculate_median(marks_dict)
print(f"Median Marks: {median_marks:.2f}")

max_student, max_score = find_max_score(marks_dict)
print(f"Highest Score: {max_student} with {max_score} marks")

min_student, min_score = find_min_score(marks_dict)
print(f"Lowest Score: {min_student} with {min_score} marks")

grade_dist=print_gradebook(marks_dict)
print("grade dictionary:",grade_dist)

distribution = grade_distribution(marks_dict) 
print(f"Grade Distribution: {distribution}")

passed, num_passed, failed, num_failed,results = pass_or_fail(marks_dict)
print(f"Passed Students ({num_passed}): {passed}")
print(f"Failed Students ({num_failed}): {failed}")
print("Results:",results)

print(print_results_table(marks_dict, grade_dist))