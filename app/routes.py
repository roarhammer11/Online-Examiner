from flask import render_template, request, redirect, url_for, flash
from app import database
from app import app, db

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

#region Create Account
@app.route("/createaccount", methods=["POST"])
def createAccount():
    if request.method == "POST":
        return render_template("createaccount.html")

@app.route("/createstudentaccount", methods=["POST"])
def createStudentAccount():
    if request.method == "POST":
        return render_template("createstudentaccount.html")

@app.route("/submitstudentform", methods=["POST"])
def submitstudentform():
    studentUsername = request.form['studentusername']
    studentPassword = request.form['studentpassword']
    #Checks if username is valid then adds to student database
    if  db.session.query(database.Student).filter(database.Student.studentUsername == studentUsername ).count() == 0:
        data = database.Student(studentUsername, studentPassword)
        db.session.add(data)
        db.session.commit()
    else:
        return render_template("createstudentaccount.html", message = 'Username is taken, please input another.')
    return render_template("index.html", message = studentUsername)
        
@app.route("/createteacheraccount", methods=["POST"])
def createTeacherAccount():
    if request.method == "POST":
        return render_template("createteacheraccount.html")

@app.route("/submitteacherform", methods=["POST"])
def submitteacherform():
    teacherUsername = request.form['teacherusername']
    teacherPassword = request.form['teacherpassword']
    #Checks if username is valid and adds to teacher database
    if db.session.query(database.Teacher).filter(database.Teacher.teacherUsername == teacherUsername ).count() == 0:
        data = database.Teacher(teacherUsername, teacherPassword)
        db.session.add(data)
        db.session.commit()
    else:
        return render_template("createteacheraccount.html", message = 'Username is taken, please input another.')
    return render_template("index.html", message = teacherUsername)
#endregion


#region Login Account
@app.route("/login", methods=["POST","GET"])
def login():
    return render_template("login.html")

@app.route("/loginstudentaccount", methods=["POST"])
def loginstudentaccount():
    if request.method == "POST":
        return render_template("loginstudentaccount.html")



@app.route("/studentlogin", methods=["POST"])
def studentLogin():
    studentUsername = request.form['studentusername']
    studentPassword = request.form['studentpassword']
    #Checks for user credibility
    if db.session.query(database.Student).filter(database.Student.studentUsername == studentUsername ).count() == 1:
        username = db.session.query(database.Student).filter_by(studentUsername = studentUsername).first()
        password = username.studentPassword
        
        if studentPassword == password:
            global name   
            name = username.studentUsername
            return render_template("studentdashboard.html", login = studentUsername)
            
    return render_template("loginstudentaccount.html", message = 'Invalid username or password')

@app.route("/loginteacheraccount", methods=["POST"])
def loginteacheraccount():
    if request.method == "POST":
        return render_template("loginteacheraccount.html")

@app.route("/teacherlogin", methods=["POST"])
def teacherLogin():
    teacherUsername = request.form['teacherusername']
    teacherPassword = request.form['teacherpassword']
    #Checks for user credibility
    if db.session.query(database.Teacher).filter(database.Teacher.teacherUsername == teacherUsername).count() == 1:
        username = db.session.query(database.Teacher).filter_by(teacherUsername = teacherUsername).first()
        password = username.teacherPassword
        if teacherPassword == password: 
            return render_template("teacherdashboard.html", login = teacherUsername)

    return render_template("loginteacheraccount.html", message = 'Invalid username or password')
#endregion

#region Dashboards
@app.route("/studentdashboard", methods=["POST", "GET"])
def studentDashboard():
    return render_template("studentdashboard.html")

#region Take Exam
@app.route("/takeexam", methods=['POST'])
def takeExam():
    if db.session.query(database.Exam).count() == 0:
        return render_template("takeexam.html", message = "Exam is empty")

    return redirect(url_for('takeExamSubmission'))

@app.route("/takeexamsubmission", methods=['POST','GET'])
def takeExamSubmission():
    questionArray = []  
    for question in db.session.query(database.Exam).order_by(database.Exam.id).all():
        questionArray.append(question.question)
    return render_template("takeexamsubmission.html", len = len(questionArray), questionarray = questionArray)  

@app.route("/examchecking", methods = ["POST","GET"])
def examchecking():
    score = 0
    studentAnswerArray = []
    answerArray = []
    for question in db.session.query(database.Exam).order_by(database.Exam.id).all():
        answerArray.append(question.answer)
        studentAnswerArray.append(request.form[question.question])
    
    for x in range(0,len(answerArray)):
        if studentAnswerArray[x] == answerArray[x]:
            score += 1

    q = "Score: {} \n"
    flash(q.format(score), category='score')
    if score >= db.session.query(database.Exam).order_by(database.Exam.question).count()*0.75: 
        flash('You passed, Good job', 'message')     
    else:
        flash('You failed, Better luck next time', 'message')
    try:
        if db.session.query(database.Score).filter(database.Score.studentname == name).count() == 0:
            data = database.Score(score, name)
            db.session.add(data)
            db.session.commit()
        else:
            username = db.session.query(database.Score).filter_by(studentname = name).first()
            username.score = score
            db.session.commit()
        return render_template("studentdashboard.html")
    except NameError:
        flash('Session error, please log in again', category='error')
        return redirect(url_for('login'))
#endregion        
        
@app.route("/teacherdashboard", methods=["POST","GET"])
def teacherDashboard():
    return render_template("teacherdashboard.html")

#region Create Exam
@app.route("/createexam", methods=["POST"])
def createExam():
    if request.method == "POST":
        return render_template("createexam.html")

@app.route("/createexamsubmission", methods = ["POST"])
def createExamSubmission():
    question = request.form['question']
    answer = request.form['answer']
    #Checks if question is not a duplicate and add to Exam database
    if db.session.query(database.Exam).filter(database.Exam.question == question ).count() == 0:
        data = database.Exam(question, answer)
        db.session.add(data)
        db.session.commit()
    else:
        return render_template("createexam.html", message = 'Cannot have duplicate questions ')
    return render_template("teacherdashboard.html", message = 'Exam Created')
#endregion

#region Edit Exam
@app.route("/editexamselection", methods=["POST","GET"])
def editexamselection():
    #Stores a list of question for the user to choose to edit
    if db.session.query(database.Exam).count() == 0:
        return render_template("teacherdashboard.html", exam = 'Exam is empty')
    questionarray = []  
    for question in db.session.query(database.Exam).order_by(database.Exam.id).all():
        questionarray.append(question.question)
    return render_template("editexamselection.html", len = len(questionarray), questionarray = questionarray)

@app.route("/editexamsubmission",methods=["POST"])
def editExamSubmission():
    editedQuestion = request.form['question']
    editedAnswer = request.form['answer']
    #Checks the question to be edited and updates the database   
    if db.session.query(database.Exam).filter(database.Exam.question == editedQuestion ).count() == 0:
        question = db.session.query(database.Exam).filter_by(question = request.form['questions']).first()
        question.question = editedQuestion
        question.answer = editedAnswer
        db.session.commit()
    else:
        questionarray = []  
        for question in db.session.query(database.Exam).order_by(database.Exam.id).all():
            questionarray.append(question.question)
        flash('Cannot duplicate questions', 'message')
        return render_template("editexamselection.html", len = len(questionarray), questionarray = questionarray)

    return render_template("teacherdashboard.html", message = 'Exam Edited')

    
#endregion

#region Delete Exam
@app.route("/deleteexamselection", methods=["POST"])
def deleteExamSelection():
    #Stores a list of question for the user to choose to delete
    if request.method == "POST":
        if db.session.query(database.Exam).count() == 0:
            return render_template("teacherdashboard.html", exam = 'Exam is empty')
        questionarray = []  
        for question in db.session.query(database.Exam).order_by(database.Exam.id).all():
            questionarray.append(question.question)
        return render_template("deleteexamselection.html", len = len(questionarray), questionarray = questionarray)

@app.route("/deleteexamsubmission",methods=["POST"])
def deleteExamSubmission():
    #Checks the question to be deleted and updates the database
    question = db.session.query(database.Exam).filter_by(question = request.form['questions']).first()
    db.session.delete(question)
    db.session.commit()
    return render_template("teacherdashboard.html", message = 'Exam Deleted')
#endregion       

# Create statistical data
@app.route("/viewstatistics", methods=["POST"])
def viewStatistics():
    if request.method == "POST":
        if db.session.query(database.Score).count() == 0:
            return render_template("teacherdashboard.html", score = 'No student took the test')
        scoreArray = []
        studentNameArray = []
        remarksArray = []
        for score in db.session.query(database.Score).order_by(database.Score.id).all():
            scoreArray.append(score.score)
    
        for studentname in db.session.query(database.Score).order_by(database.Score.id).all():
            studentNameArray.append(studentname.studentname)

        for remarks in scoreArray:
            if float(remarks) >= db.session.query(database.Exam).order_by(database.Exam.question).count()*0.75:
                remarksArray.append("Passed")
            else:
                remarksArray.append("Failed")
        return render_template("viewstatistics.html", len = len(studentNameArray), scoreArray = scoreArray, studentNameArray = studentNameArray, remarksArray = remarksArray)
#endregion
