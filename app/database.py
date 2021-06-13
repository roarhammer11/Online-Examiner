from app import db
#region Databases
class Teacher(db.Model):
    __tablename__ = 'Teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacherUsername = db.Column(db.String(200), unique=True, nullable=False)
    teacherPassword = db.Column(db.String(200), nullable=False)

    def __init__(self, teacherUsername, teacherPassword):
        self.teacherUsername = teacherUsername
        self.teacherPassword = teacherPassword

class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    studentUsername = db.Column(db.String(200), unique=True, nullable=False)
    studentPassword = db.Column(db.String(200), nullable=False)

    def __init__(self, studentUsername, studentPassword):
        self.studentUsername = studentUsername
        self.studentPassword = studentPassword

class Exam(db.Model):
    __tablename__ = 'Exam'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), unique=True, nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    def __init__(self, question, answer):
        self.answer = answer
        self.question = question

class Score(db.Model):
    __tablename__ = 'Score'
    id = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.String(200), unique=True, nullable=False)
    score = db.Column(db.String(200), nullable=False)

    def __init__(self, score, studentname):
        self.score = score
        self.studentname = studentname
#endregion