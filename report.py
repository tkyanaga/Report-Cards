
import csv

# -------------------------Functions-------------------------
def processTestWeights(testPercentages, courseList):
	try:
		with open('tests.csv', newline='') as csvfile:
			testReader = csv.reader(csvfile, delimiter=',')

			col = 0
			for row in testReader:
				if col == 0 or not any(row):
					col += 1
					continue
				if not row:
				 	exit(2)
				#stores total percent of courses
				prev = courseList.get(row[1], 0)
				courseList[row[1]] = int(row[2]) + prev
				#stores test id as key and (percent of grade, course_id) as value
				testPercentages[int(row[0])] = (int(row[2])/100, row[1])

			for count, (key, total) in enumerate(courseList.items()):
				if total is not 100:
					print("Error, the sum of the test weights for course number ", str(count + 1), "does not equal 100, but ", str(total))
					exit(1)
	except IOError:
		print('tests.csv not loaded')
		exit(2)


def processStudents(students):
	try:
		with open('students.csv', newline='') as csvfile:
			stuReader = csv.reader(csvfile, delimiter=',')

			col = 0
			for row in stuReader:
				if col == 0 or not any(row):
					col += 1
					continue
				#index starts at 1
				students[int(row[0])] = row[1]
	except IOError:
		print('students.csv not loaded')
		exit(3)

def processCourses(courses):
	try:
		with open('courses.csv', newline='') as csvfile:
			courseReader = csv.reader(csvfile, delimiter=',')

			col = 0
			for row in courseReader:
				if col == 0 or not any(row):
					col += 1
					continue
				
					
				#index starts at 1
				courses[row[0]] = (row[1], row[2])
	except IOError:
		print('courses.csv not loaded')
		exit(4)

def processMarks(marks):
	try:
		with open('marks.csv', newline='') as csvfile:
			marksReader = csv.reader(csvfile, delimiter=',')

			col = 0
			for row in marksReader:
				if col == 0 or not any(row):
					col += 1
					continue
				#	(test_id, student_id)
				key = (int(row[0]), int(row[1]))
				#	key		mark (could've put in mark*test percent, but all math in calc function)
				mark = int(row[2])
				if mark < 0 or mark > 100:
					print(f"Mark {row[2]} for student {row[1]}, test {row[0]} is out of range [0,100]")
				marks[key] = int(row[2])
	except IOError:
		print('marks.csv not loaded')
		exit(5)

def calculateCourseTotal(marks, testPercentages, studentGrades, studentCourses, studentTotalScore = []):
	#to populate studentGrades and studentTotalScore
	for ((test_id,student_id), mark) in marks.items():
		(weight, course_id) = testPercentages[test_id]

		curr_grade = mark * weight
		#returns 0 if no key found
		prev_grade = studentGrades.get((student_id, course_id), 0)
		studentGrades[(student_id, course_id)] = curr_grade + prev_grade


	for ((student_id, course_id), grade) in studentGrades.items():
		studentTotalScore[int(student_id) - 1] += grade
		
		if student_id in studentCourses:
			studentCourses[student_id].append((course_id, grade))
		else:
			studentCourses[student_id] = [(course_id, grade)]



def createOutputForStudent(student_id, studentCourses, students, courses, studentTotal):
	output = f"Student Id: {student_id}, name: {students[student_id]}\n"
	avg = studentTotalScore[student_id - 1]/len(studentCourses)
	avg = "{:.2f}".format(avg)
	output += f"Total Average:\t{avg}%\n\n"
	for course_id, grade in studentCourses:
		course, teacher = courses[str(course_id)]
		grade = "{:.2f}".format(grade)
		output += f"\tCourse: {course}, Teacher: {teacher}\n"
		output += f"\tFinal Grade:\t{grade}\n\n"

	output += "\n\n"
	return output

# -------------------------Code-------------------------

#key: student_id
#value: name
students = {}

#key: course_id 
#value:(name, teacher)
courseList = {}

courses = {}

#key: test_id 
#value: (percent weight, course_id)
testPercentages = {}

#key:(test_id, student_id) 
#value: mark
marks = {}

#key: (student_id, course_id) 
#value: final grade
studentGrades = {}

#key: student_id 
#value: [(course_id, grade)]
studentCourses = {}

processStudents(students)
processCourses(courses)

#sum of each course score
studentTotalScore = [0]*len(students)

processTestWeights(testPercentages, courseList)
processMarks(marks)

calculateCourseTotal(marks, testPercentages, studentGrades, studentCourses, studentTotalScore)

# create a sorted list of ids
ids = tuple(s for s in students)
ids = sorted(ids)
#sort each students list of courses
for student_id in ids:
	studentCourses[student_id] = sorted(studentCourses[student_id], key=str)

#open file and write each student's information
reportCard = open("report_card.txt", "w")
for student_id in ids:
	reportCard.write(createOutputForStudent(student_id, studentCourses[student_id], students, courses, studentTotalScore))
