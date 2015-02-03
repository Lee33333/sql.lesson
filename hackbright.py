import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Title: %s 
    Description: %s"""% (row[0], row[1])

def get_grade_by_title(title):
    query = """ SELECT project_title, grade FROM Grades WHERE project_title = ?"""
    DB.execute(query,(title,))
    row = DB.fetchone()
    print """\
    Title: %s
    Grade: %s """ % (row[0], row[1])

def show_all_grades(last_name, first_name):
    query = """ SELECT first_name, last_name, grade FROM Students INNER JOIN Grades ON (Students.github = Grades.student_github) WHERE last_name = ? AND first_name = ?"""
    DB.execute(query, ((last_name,first_name,)))
    results = DB.fetchall()
    for row in results:
        print """\
        First: %s
        Last: %s
        Grade: %s \n""" % (row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def add_new_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s" % (title, description, max_grade)

def add_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s %s %s" % (student_github, project_title, grade)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            add_new_project(*args)
        elif command == "grade":
            get_grade_by_title(*args)
        elif command == "new_grade":
            add_grade(*args)
        elif command == "allgrades":
            show_all_grades(*args)

    CONN.close()



if __name__ == "__main__":
    main()
