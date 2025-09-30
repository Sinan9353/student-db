from flask import Flask, render_template, request, redirect, url_for
from models import db, Student

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-secure-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create database if not exists
with app.app_context():
    db.create_all()

# ---------------- Routes ---------------- #

@app.route('/')
def index():
    students = Student.query.order_by(Student.id).all()
    return render_template("index.html", students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        course = request.form['course']
        
        # Optional: check duplicates
        existing = Student.query.filter((Student.roll_no==roll_no) | (Student.email==email)).first()
        if existing:
            return "Error: Roll No or Email already exists!"
        
        student = Student(name=name, roll_no=roll_no, email=email, course=course)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("add_student.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_no = request.form['roll_no']
        student.email = request.form['email']
        student.course = request.form['course']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("edit_student.html", student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
