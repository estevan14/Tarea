import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estudiante1.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


# modelado
class estudiantes(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    apellido = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<nombre: {}>".format(self.nombre)


# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        student = estudiantes(nombre=request.form.get("nombre"), apellido=request.form.get("apellido"))
        db.session.add(student)
        db.session.commit()

    students = estudiantes.query.all()
    return render_template("home.html", students=students)
    # return render_template("home.html")


@app.route("/update", methods=["POST"])
def update():
    nombre = request.form.get("nombre")
    id = request.form.get("id")
    apellido = request.form.get("apellido")
    student = estudiantes.query.get(id)
    student.nombre = nombre
    student.apellido=apellido
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    student = estudiantes.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
