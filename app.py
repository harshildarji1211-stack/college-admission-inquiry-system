from flask import Flask, render_template, request, redirect, session
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "college_admission_secret_key"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# COURSES PAGE
# =========================

@app.route("/courses")
def courses():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM courses ORDER BY course_id"
    )

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "courses.html",
        courses=courses
    )


# =========================
# ADMISSION PAGE
# =========================

@app.route("/admission", methods=["GET", "POST"])
def admission():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM courses ORDER BY course_id"
    )

    courses = cursor.fetchall()

    if request.method == "POST":

        student_name = request.form["student_name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        course = request.form["course"]
        qualification = request.form["qualification"]
        percentage = request.form["percentage"]
        address = request.form["address"]

                # Save student information
        cursor.execute(
            """
            INSERT INTO students
            (
                student_name,
                email,
                mobile,
                address,
                qualification,
                percentage
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                student_name,
                email,
                mobile,
                address,
                qualification,
                percentage
            )
        )


        # Save admission application
        cursor.execute(
            """
            INSERT INTO applications
            (
                student_name,
                email,
                mobile,
                course,
                qualification,
                percentage,
                address
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                student_name,
                email,
                mobile,
                course,
                qualification,
                percentage,
                address
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        return "Application Submitted Successfully! ✅"

    cursor.close()
    connection.close()

    return render_template(
        "admission.html",
        courses=courses
    )


# =========================
# INQUIRY PAGE
# =========================

@app.route("/inquiry", methods=["GET", "POST"])
def inquiry():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM courses ORDER BY course_id"
    )

    courses = cursor.fetchall()

    if request.method == "POST":

        student_name = request.form["student_name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        course = request.form["course"]
        message = request.form["message"]

        cursor.execute(
            """
            INSERT INTO inquiries
            (
                student_name,
                email,
                mobile,
                course,
                message
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                student_name,
                email,
                mobile,
                course,
                message
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "Inquiry Submitted Successfully! ✅"

    cursor.close()
    connection.close()

    return render_template(
        "inquiry.html",
        courses=courses
    )


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM admin
            WHERE username = %s AND password = %s
            """,
            (username, password)
        )

        admin = cursor.fetchone()

        cursor.close()
        connection.close()

        if admin:

            session["admin_logged_in"] = True
            session["admin_username"] = username

            return redirect("/admin/dashboard")

        else:
            return "Invalid Username or Password ❌"

    return render_template("login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get applications
    cursor.execute(
        "SELECT * FROM applications ORDER BY application_id DESC"
    )

    applications = cursor.fetchall()

    # Get inquiries
    cursor.execute(
        "SELECT * FROM inquiries ORDER BY inquiry_id DESC"
    )

    inquiries = cursor.fetchall()

    # Get courses
    cursor.execute(
        "SELECT * FROM courses ORDER BY course_id DESC"
    )

    courses = cursor.fetchall()

    # =========================
    # DASHBOARD STATISTICS
    # =========================

    cursor.execute(
        "SELECT COUNT(*) AS total FROM applications"
    )

    total_applications = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM applications
        WHERE status = 'Pending'
        """
    )

    pending_applications = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS total FROM inquiries"
    )

    total_inquiries = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS total FROM courses"
    )

    total_courses = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return render_template(
        "admin_dashboard.html",
        applications=applications,
        inquiries=inquiries,
        courses=courses,
        total_applications=total_applications,
        pending_applications=pending_applications,
        total_inquiries=total_inquiries,
        total_courses=total_courses
    )


# =========================
# UPDATE INQUIRY STATUS
# =========================

@app.route("/update_inquiry_status", methods=["POST"])
def update_inquiry_status():

    inquiry_id = request.form["inquiry_id"]
    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE inquiries
        SET status = %s
        WHERE inquiry_id = %s
        """,
        (status, inquiry_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin/dashboard")


# =========================
# UPDATE APPLICATION STATUS
# =========================

@app.route("/update_application_status", methods=["POST"])
def update_application_status():

    application_id = request.form["application_id"]
    status = request.form["status"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET status = %s
        WHERE application_id = %s
        """,
        (status, application_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin/dashboard")


# =========================
# ADD COURSE
# =========================

@app.route("/add_course", methods=["POST"])
def add_course():

    course_name = request.form["course_name"]
    duration = request.form["duration"]
    eligibility = request.form["eligibility"]
    fees = request.form["fees"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO courses
        (
            course_name,
            duration,
            eligibility,
            fees
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            course_name,
            duration,
            eligibility,
            fees
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin/dashboard")


# =========================
# EDIT COURSE PAGE
# =========================

@app.route("/edit_course/<int:course_id>")
def edit_course(course_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM courses
        WHERE course_id = %s
        """,
        (course_id,)
    )

    course = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_course.html",
        course=course
    )


# =========================
# UPDATE COURSE
# =========================

@app.route("/update_course/<int:course_id>", methods=["POST"])
def update_course(course_id):

    course_name = request.form["course_name"]
    duration = request.form["duration"]
    eligibility = request.form["eligibility"]
    fees = request.form["fees"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE courses
        SET
            course_name = %s,
            duration = %s,
            eligibility = %s,
            fees = %s
        WHERE course_id = %s
        """,
        (
            course_name,
            duration,
            eligibility,
            fees,
            course_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin/dashboard")


# =========================
# DELETE COURSE
# =========================

@app.route("/delete_course/<int:course_id>", methods=["POST"])
def delete_course(course_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM courses
        WHERE course_id = %s
        """,
        (course_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/admin/dashboard")
# =========================
# ADMIN LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)