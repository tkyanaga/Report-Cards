README
To run place script in the folder containing the following files:
  courses.csv
  marks.csv
  students.csv
  tests.csv
Then from the terminal, change into the directory containing the script and the above mentioned 4 files and type:
	python report.py

Once the script has finished, in the same folder a 
  report_card.txt 
will appear. That is the output!

Exit status:
0 - success
1 - test weights of at least one course do not sum to 100
2 - 'tests.csv' file not found
3 - 'students.csv' file not found
4 - 'courses.csv' file not found
5 - 'marks.csv' file not found

Description:
This program will take 4 files containing information about students, their courses, their marks, and their tests then it will generate a report card file. 

This file contains each student, ordered by their student id, their overall grade, each course they took and their grade, course title and teacher.