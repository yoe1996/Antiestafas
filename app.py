from flask import Flask, render_template, request, redirect
from config import Config
from models import db, User, Report
from auth import auth, bcrypt
from flask_login import LoginManager, login_required

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/dashboard")
@login_required
def dashboard():
    total = Report.query.count()
    return render_template("dashboard.html", total=total)

@app.route("/report", methods=["GET","POST"])
@login_required
def report():
    if request.method == "POST":
        r = Report(
            titulo=request.form["titulo"],
            categoria=request.form["categoria"],
            descripcion=request.form["descripcion"],
            monto=request.form["monto"],
            fecha=request.form["fecha"],
            contacto=request.form["contacto"],
            estafador=request.form["estafador"],
            telefono=request.form["telefono"],
            direccion=request.form["direccion"],
            tarjeta=request.form["tarjeta"],
            provincia=request.form["provincia"]
        )
        db.session.add(r)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("report.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
