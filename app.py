from flask import Flask, render_template, request

app = Flask(__name__)

class Subject :
    def __init__ (self, name, cred, sem) :
        self.name = name
        self.cred = int(cred)
        self.sem = int(sem)

class Grade :
    def __init__ (self, g) :
        self.g = g

class Marks(Grade, Subject) :

    def __init__ (self, mis, m) :
        self.mis = int(mis)
        self.m = m
        self.str_grade = []
        self.pointer = []
        self.to_return = []
        self.total_creds = 0
        self.cgpa = 0

    def calc_grade(self, grades, subs) :
        str_grades_library = ['FF', 'DD', 'CD', 'CC', 'BC', 'BB', 'AB', 'AA']
        for i in range(len(self.m)) :
            self.total_creds += int(subs[i].cred)
            for j in range(len(grades[i].g)) :
                if (float(self.m[i]) < float(grades[i].g[j])) :
                    break
            self.str_grade.append(str_grades_library[j])
            if (j > 0) :
                j += 3
            self.pointer.append(j)
            self.cgpa += self.pointer[i]
        self.cgpa = self.cgpa / self.total_creds

        for i in range(len(self.m)) :
            self.to_return.append({
                'name' : subs[i].name,
                'credits' : subs[i].cred,
                'grade' : self.str_grade[i],
                'grade_point' : self.pointer[i]})


subs = []
grades = []
marks = []
i = 0

with open('subjects.csv', 'r') as f1 :
    line = ''
    line = f1.readline()
    while line :
        data = line.split(',')
        subs.append(Subject(data[0], data[1], data[2]))
        line = f1.readline()

with open('grades.csv', 'r') as f2 :
    line = ''
    line = f2.readline()
    while line :
        data = line.split(',')
        data.append('100')
        grades.append(Grade(data))
        line = f2.readline()

with open('marks.csv', 'r') as f3 :
    line = ''
    line = f3.readline()
    while line :
        data = line.split(',')
        marks.append(Marks(data[0], data[1:]))
        line = f3.readline()

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/report', methods = ['POST'])
def report() :
    prompt_mis = int(request.form['student_id'])

    for i in range(len(marks)) :
        if (int(marks[i].mis) == prompt_mis) :
            break
    marks[i].calc_grade(grades,subs)
    print(marks[i].cgpa)

    return render_template(
            'result.html',
            student_id = marks[i].mis,
            subjects = marks[i].to_return,
            cgpa = marks[i].cgpa
        )

if __name__ == '__main__':
    app.run(debug=True)





