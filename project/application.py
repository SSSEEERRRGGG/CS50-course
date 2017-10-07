from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime, date, time


from helpers import *
                                                                        # configure application
app = Flask(__name__)
                                                                        # ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


                                                                        # configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
                                                                        # configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/main_page")
@login_required
def index():
    count = db.execute("SELECT count(*) from diary WHERE id=:id", id=session["user_id"])
    c_list = str(count)
    length = len(c_list)
    if length==17:
	    a = c_list[14:15]
    elif length==18:
	    a = c_list[14:16]
    if c_list[14:15]=="1":
        b = "entry"
    else:
        b = "entries"
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])
    return render_template("index1.html", name=name, count=str(a), b=b)


@app.route("/about")
@login_required
def about_us():
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])
    return render_template("about_us.html", name=name)

@app.route("/support")
@login_required
def support():
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])
    return render_template("support.html", name=name)

@app.route("/helpFAQ")
@login_required
def helpFAQ():
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])
    return render_template("helpFAQ.html", name=name)


@app.route("/history")
@login_required
def history():
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])

    count = db.execute("SELECT count(*) from diary WHERE id=:id", id=session["user_id"])
    c_list = str(count)
    length = len(c_list)
    if length==17:
	    a = c_list[14:15]
    elif length==18:
	    a = c_list[14:16]
    if c_list[14:15]=="1":
        b = "entry"
    else:
        b = "entries"

    histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
    diary = db.execute("SELECT * from diary WHERE id=:id", id=session["user_id"])
    return render_template("history.html", histories=histories, diary=diary, name=name, count=str(a), b=b)


@app.route("/start")
def start():
    session.clear()
    return render_template("start.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()                                                     # forget any user_id

    if request.method == "POST":                                        # if user reached route via POST (as by submitting a form via POST)

        if not request.form.get("username"):                            # ensure username was submitted
            flash("No username")
            return redirect(url_for("login"))

        elif not request.form.get("password"):                          # ensure password was submitted
            flash("No password")
            return redirect(url_for("login"))
                                                                        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
                                                                        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return flash("Username or password doesn`t exist")
            return redirect(url_for("login"))

        session["user_id"] = rows[0]["id"]                              # remember which user has logged in

        return redirect(url_for("index"))                               # redirect user to home page

    else:                                                               # else if user reached route via GET (as by clicking a link or via redirect)
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()                                                     # forget any user_id
    return redirect(url_for("start"))                                   # redirect user to login form


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must provide username")# ensure username was submitted
            return redirect(url_for("register"))

        elif not request.form.get("password"):
            flash("Must provide password")# ensure password was submitted
            return redirect(url_for("register"))
                                                                        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            flash("Password doesn't match")
            return redirect(url_for("register"))
                                                                        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", \
                             username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        if not result:
            return redirect(url_for("register"))

        session["user_id"] = result                                     # remember which user has logged in

        return redirect(url_for("index"))                               # redirect user to home page

    else:
        return render_template("register.html")




@app.route("/entry", methods=["GET", "POST"])
@login_required
def index_entry():
    now_date = datetime.today() # Текущая дата (без времени)
    now_time = datetime.now() # Текущая дата со временем
    cur_y = now_date.year
    cur_mon = now_date.month # Месяц текущий
    cur_d = now_date.day
    cur_h = now_time.hour # Час текущий
    cur_m = now_time.minute # Минута текущая
    cur_s = now_time.second
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])

    if request.method == "POST":
        q = request.form.get("title")
        qq = request.form.get("editor_1")
        db.execute("INSERT INTO diary (title, editor, sliced_editor, id) VALUES(:title, :editor, :sliced_editor, :id)", \
                    title=q, editor=request.form.get("editor_1"), sliced_editor=request.form.get("editor_1")[0:150]+"...", id=session["user_id"])

        db.execute("INSERT INTO histories (title, editor, id) VALUES(:title, :editor, :id)", \
                    title=request.form.get("title"), editor=request.form.get("editor_1"), id=session["user_id"])

        editor = db.execute("SELECT editor FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)
        title = db.execute("SELECT title FROM diary WHERE id=:id AND editor=:editor", id=session["user_id"], editor=qq)
        time = db.execute("SELECT time FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)

        c = len(str(qq))
        f = str(qq)
        ct = 0; flag = 0
        for i in range(len(f)):
            if f[i] != ' ' and flag == 0:
                ct += 1
                flag = 1
            else:
                if f[i] == ' ':
                    flag = 0
        words = "Words:"
        return render_template("open.html", editor=qq, title=q, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, time=time, name=name, c=str(c), ct=str(ct), words=words)
    else:
        #q = request.form.get("title")
        #qq = request.form.get("editor_1")
        editor = db.execute("SELECT editor FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=request.form.get("title"))
        title = db.execute("SELECT title FROM diary WHERE id=:id AND editor=:editor", id=session["user_id"], editor=request.form.get("editor_1"))
        time = db.execute("SELECT time FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=request.form.get("title"))
        return render_template("open.html", time=time, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, cur_h=cur_h, cur_m=cur_m, name=name)#, editor=qq, title=q, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, cur_h=cur_h, cur_m=cur_m, time=time)



@app.route("/open_entry", methods=["GET", "POST"])
#@login_required
def open_entry():
    now_date = datetime.today() # Текущая дата (без времени)
    now_time = datetime.now() # Текущая дата со временем
    cur_y = now_date.year
    cur_mon = now_date.month # Месяц текущий
    cur_d = now_date.day
    cur_h = now_time.hour # Час текущий
    cur_m = now_time.minute # Минута текущая
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])



    if request.method == "GET":
        return render_template("open.html", name=name)
    else:
        q = request.form.get("title")
        qq = request.form.get("sliced")

        #db.execute("INSERT INTO diary (title, editor, sliced_editor, id) VALUES(:title, :editor, :sliced_editor, :id)", \
          #          title=q, editor=request.form.get("editor_1"), sliced_editor=request.form.get("editor_1")[0:92]+"...", id=session["user_id"])
        db.execute("INSERT INTO histories (title, editor, id) VALUES(:title, :editor, :id)", \
                    title=request.form.get("title"), editor=request.form.get("sliced"), id=session["user_id"])
        editor = db.execute("SELECT editor FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)
        #title = db.execute("SELECT title FROM diary WHERE id=:id AND sliced_editor=:sliced_editor", id=session["user_id"], sliced_editor=qq)
        time = db.execute("SELECT time FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)


        return render_template("open1.html", editor=editor, title=q, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, cur_h=cur_h, cur_m=cur_m, time=time, name=name)#,  c=str(c), ct=str(ct), f=f)

@app.route("/delete", methods=["GET", "POST"])
#@login_required
def delete():
    now_date = datetime.today() # Текущая дата (без времени)
    now_time = datetime.now() # Текущая дата со временем
    cur_y = now_date.year
    cur_mon = now_date.month # Месяц текущий
    cur_d = now_date.day
    cur_h = now_time.hour # Час текущий
    cur_m = now_time.minute # Минута текущая
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])

    count = db.execute("SELECT count(*) from diary WHERE id=:id", id=session["user_id"])
    c_list = str(count)
    length = len(c_list)
    if length==17:
	    a = c_list[14:15]
    elif length==18:
	    a = c_list[14:16]
    if c_list[14:15]=="1":
        b = "entry"
    else:
        b = "entries"

    words = "Words:"

    if request.method == "GET":
        return render_template("support.html")
    else:
        q = request.form.get("title")
        db.execute("DELETE FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)

        editor = db.execute("SELECT editor FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)
        #title = db.execute("SELECT title FROM diary WHERE id=:id AND sliced_editor=:sliced_editor", id=session["user_id"], sliced_editor=qq)
        time = db.execute("SELECT time FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)

        histories = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
        diary = db.execute("SELECT * from diary WHERE id=:id", id=session["user_id"])
        return render_template("history.html", editor=editor, title=q, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, cur_h=cur_h, cur_m=cur_m, time=time, histories=histories, diary=diary, name=name, count=str(a), b=b, words=words)




@app.route("/open", methods=["GET", "POST"])
#@login_required
def index_open():
    now_date = datetime.today() # Текущая дата (без времени)
    now_time = datetime.now() # Текущая дата со временем
    cur_y = now_date.year
    cur_mon = now_date.month # Месяц текущий
    cur_d = now_date.day
    cur_h = now_time.hour # Час текущий
    cur_m = now_time.minute # Минута текущая
    cur_s = now_time.second
    saved = "Saved:"
    name = db.execute("SELECT username from users WHERE id=:id", id=session["user_id"])
    if request.method == "GET":
        return render_template("open.html", name=name)
    else:
        q = request.form.get("title")
        qq = request.form.get("editor_1")
        db.execute("INSERT INTO diary (title, editor, sliced_editor, id) VALUES(:title, :editor, :sliced_editor, :id)", \
                    title=q, editor=request.form.get("editor_1"), sliced_editor=request.form.get("editor_1")[0:150]+"...", id=session["user_id"])
        db.execute("INSERT INTO histories (title, editor, id) VALUES(:title, :editor, :id)", \
                    title=request.form.get("title"), editor=request.form.get("editor_1"), id=session["user_id"])

        editor = db.execute("SELECT editor FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)
        title = db.execute("SELECT title FROM diary WHERE id=:id AND editor=:editor", id=session["user_id"], editor=qq)
        time = db.execute("SELECT time FROM diary WHERE id=:id AND title=:title", id=session["user_id"], title=q)

        dt = str(now_time)
        db.execute("UPDATE diary SET editor=:editor, sliced_editor=:sliced_editor WHERE id=:id AND title=:title", \
                    editor=request.form.get("editor_1"), title=request.form.get("title"), sliced_editor=request.form.get("editor_1")[0:150]+"...", id=session["user_id"])
        db.execute("UPDATE diary SET time=:time WHERE id=:id AND title=:title", \
                    time = dt[:19], title=request.form.get("title"), id=session["user_id"])

        c = len(str(qq))
        f = str(qq)
        ct = 0; flag = 0
        for i in range(len(f)):
            if f[i] != ' ' and flag == 0:
                ct += 1
                flag = 1
            else:
                if f[i] == ' ':
                    flag = 0
        words = "Words:"
        return render_template("open.html", editor=qq, title=q, cur_y=cur_y, cur_mon=cur_mon, cur_d=cur_d, cur_h=cur_h, cur_m=cur_m, time=time, saved=saved, name=name, c=str(c), ct=str(ct), words=words)

