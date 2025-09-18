from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from flask import send_from_directory
import os
from mysql.connector import pooling
from werkzeug.utils import secure_filename
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_CONFIG = {
    'host': 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
    'user': '2tJ2hbMoj1vsu2d.root',
    'password': 'sYvHNm8s96kZnXQN',
    'database': 'newproject',
}

pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **DB_CONFIG)

def get_db_connection():
    return pool.get_connection()
# --- First app routes ---

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/page2-1')
def page2_1():
    return render_template('page2-1.html')

@app.route('/page2-2')
def page2_2():
    return render_template('page2-2.html')

@app.route('/page2-3')
def page2_3():
    return render_template('page2-3.html')

@app.route('/page2-4')
def page2_4():
    return render_template('page2-4.html')

@app.route('/page2-5')
def page2_5():
    return render_template('page2-5.html')

@app.route('/page2-6')
def page2_6():
    return render_template('page2-6.html')

# --- Second app routes ---

@app.route('/page3-1')
def page3_1():
    return render_template('page3-1.html')

@app.route('/page3-2')
def page3_2():
    return render_template('page3-2.html')

@app.route('/page3-3')
def page3_3():
    return render_template('page3-3.html')

# --- Third app routes ---

@app.route('/page4-1')
def page4_1():
    return render_template('page4-1.html')

@app.route('/page4-2')
def page4_2():
    return render_template('page4-2.html')

@app.route('/page4-3')
def page4_3():
    return render_template('page4-3.html')

# --- fourth app routes ---

@app.route('/page5-1')
def page5_1():
    return render_template('page5-1.html')

@app.route('/page5-2')
def page5_2():
    return render_template('page5-2.html')

@app.route('/page5-3')
def page5_3():
    return render_template('page5-3.html')

# --- fifth app routes ---

@app.route('/page6-1')
def page6_1():
    return render_template('page6-1.html')

# --- Import Students from Excel (Bulk) ---
@app.route('/import_students', methods=['POST'])
def import_students():
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    if not user_ids or not isinstance(user_ids, list):
        return jsonify({'success': False, 'error': 'No user_ids provided.'}), 400
    results = {'inserted': [], 'skipped': [], 'errors': []}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for user_id in user_ids:
            try:
                # Check if user already exists
                cursor.execute("SELECT user_id FROM login1 WHERE user_id = %s", (user_id,))
                if cursor.fetchone():
                    results['skipped'].append(user_id)
                    continue
                # Insert new student with default password 'AIML'
                cursor.execute("INSERT INTO login1 (user_id, password) VALUES (%s, %s)", (user_id, 'AIML'))
                results['inserted'].append(user_id)
            except Exception as e:
                results['errors'].append({'user_id': user_id, 'error': str(e)})
        conn.commit()
        cursor.close()
        conn.close()
        if results['errors']:
            return jsonify({'success': False, 'error': 'Some users failed to import.', 'details': results}), 207
        return jsonify({'success': True, 'details': results}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/page6-2')
def page6_2():
    return render_template('page6-2.html')

@app.route('/page6-3')
def page6_3():
    return render_template('page6-3.html')

# --- sixth app routes ---

@app.route('/page7-1')
def page7_1():
    return render_template('page7-1.html')

@app.route('/page7-2')
def page7_2():
    return render_template('page7-2.html')

@app.route('/page7-3')
def page7_3():
    return render_template('page7-3.html')

# --- seventh app routes ---

@app.route('/page8-2')
def page8_2():
    return render_template('page8-2.html')

@app.route('/page8-3')
def page8_3():
    return render_template('page8-3.html')

def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("Connected to MySQL database")
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None
    
# --- Authentication Routes ---
def login_user(table, success_page):
    userid = request.form['userid']
    password = request.form['password']
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {table} WHERE user_id = %s AND password = %s"
            cursor.execute(query, (userid, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = userid  # Set the session variable for logged-in user
                return redirect(url_for(success_page))
            else:
                return "Invalid Credentials", 401
        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500

@app.route('/login', methods=['POST'])
def login():
    return login_user('login1', 'page4')

@app.route('/dept-login', methods=['POST'])
def dept_login():
    return login_user('dept', 'page4_dept')

@app.route('/faculty-login', methods=['POST'])
def faculty_login():
    return login_user('faculty', 'page4_faculty')

@app.route('/studentclubs-login', methods=['POST'])
def studentclubs_login():
    return login_user('studentclubs', 'page4_studentclubs')

@app.route('/startups-login', methods=['POST'])
def startups_login():
    return login_user('startups', 'page4_startups')

@app.route('/hods-login', methods=['POST'])
def hods_login():
    return login_user('hods', 'page4_hods')

# --- Page Rendering Routes ---
@app.route('/page4')
def page4():
    return render_template('page25-3.html')

@app.route('/page4-dept')
def page4_dept():
    return render_template('page25-1.html')

@app.route('/page4-faculty')
def page4_faculty():
    return render_template('page25-2.html')

@app.route('/page4-studentclubs')
def page4_studentclubs():
    return render_template('page25-4.html')

@app.route('/page4-startups')
def page4_startups():
    return render_template('page25-5.html')

@app.route('/page4-hods')
def page4_hods():
    return render_template('page25-6.html')

@app.route('/hods/faculty-profile')
def hods_faculty_profile():
    return render_template('page25-6-faculty-profile.html')

@app.route('/hods/student-profile')
def hods_student_profile():
    return render_template('page25-6-student-profile.html')

@app.route('/hods/department-profile')
def hods_department_profile():
    return render_template('page25-6-department-profile.html')

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/get_startups', methods=['GET'])
def get_startups():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, foundation_date, industry_sector, current_stage, website_link, founder_details, overview, financial_details, market_competition, product_service_details, additional_info FROM start_ups")
        startups = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(startups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/submit1', methods=['POST'])
def submit1():
    if request.method == 'POST':
        startup_name = request.form['startupName']
        foundation_date = request.form['startupfoundationdate']
        industry_sector = request.form['startupindustrysector']
        current_stage = request.form['StartupCurrentstage']
        website_link = request.form['Startuplink']
        founder_details = request.form['studentfounderdetailsdate']
        overview = request.form['startupoverview']
        financial_details = request.form['financialdetails']
        market_competition = request.form['marketandcompetition']
        product_service_details = request.form['productorservicedetails']
        additional_info = request.form['startupadditionalinformation']
        timestamp = datetime.now()
        null_column1 = None
        null_column2 = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = '''INSERT INTO start_ups
                    (name, foundation_date, industry_sector, current_stage, website_link, founder_details, overview, financial_details, market_competition, product_service_details, additional_info, timestamp, null_column1, null_column2) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (startup_name, foundation_date, industry_sector, current_stage, website_link, founder_details, overview, financial_details, market_competition, product_service_details, additional_info, timestamp, null_column1, null_column2)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            flash('Startup details submitted successfully!', 'success')
        except Exception as e:
            flash(f'Error submitting details: {e}', 'danger')
        
        return redirect(url_for('page4_startups'))
    
@app.route('/login2', methods=['POST'])
def login2():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE startups SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500
    
@app.route('/submit2', methods=['POST'])
def submit2():
    club_name = request.form['clubName']
    coordinator_name = request.form['coordinatorName']
    event_name = request.form['Eventname']
    event_type = request.form['clubeventtype']
    venue = request.form['Venue']
    start_date = request.form['sdate']
    start_time = request.form['stime']
    end_date = request.form['edate']
    end_time = request.form['etime']
    extra_details = request.form['ExtraDetails']
    organiser_name = request.form['Organisingbody']
    organiser_details = request.form['Odetails']
    beneficiaries = request.form['Beneficiaries']
    remarks = request.form['remarks']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO event_details (club_name, coordinator_name, event_name, event_type, venue, start_date, start_time, 
                end_date, end_time, extra_details, organiser_name, organiser_details, beneficiaries, remarks) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (club_name, coordinator_name, event_name, event_type, venue, start_date, start_time, end_date, end_time, extra_details, organiser_name, organiser_details, beneficiaries, remarks))
            conn.commit()
            flash('Submitted Successfully!', 'success')
        except mysql.connector.Error as e:
            flash(f'Database Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('page4_studentclubs'))

@app.route('/get_events', methods=['GET'])
def get_events():
    # Get the organiser_name from the query parameters
    organiser_name = request.args.get('organiser_name')

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT club_name, coordinator_name, event_name, event_type, venue, 
                start_date, start_time, end_date, end_time, extra_details, 
                organiser_name, organiser_details, beneficiaries, remarks 
                FROM event_details
                WHERE organiser_name = %s
            """
            cursor.execute(query, (organiser_name,))
            events = cursor.fetchall()

            # Convert non-serializable objects (e.g., timedelta) to strings
            for event in events:
                for key, value in event.items():
                    if isinstance(value, timedelta):
                        event[key] = str(value)  # Convert timedelta to string

            return jsonify(events)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/login4', methods=['POST'])
def login4():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE studentclubs SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500

@app.route('/login3', methods=['POST'])
def login3():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE hods SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500

@app.route('/login5', methods=['POST'])
def login5():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE login1 SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500
    
@app.route('/get_patents', methods=['GET'])
def get_patents():
    department = request.args.get('department')

    if not department:
        return jsonify({'error': 'Department is required'}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, applicant_name, inventors, department, patent_title, patent_number, 
                   status, filed_date, published_date, granted_date
            FROM patents
            WHERE department = %s
        """
        cursor.execute(query, (department,))
        patents = cursor.fetchall()

        # Convert timedelta fields to string for JSON serialization
        for patent in patents:
            for key, value in patent.items():
                if isinstance(value, timedelta):
                    patent[key] = str(value)

        return jsonify(patents)
    
    except Error as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/get_publications_journals', methods=['GET'])
def get_publications_journals():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, journal_type, authors, journal_name, paper_title, issn, quartile_ranking, doi, volume, page, month_year
                FROM publications
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            publications = cursor.fetchall()

            # Convert non-serializable objects to strings
            for publication in publications:
                for key, value in publication.items():
                    if isinstance(value, timedelta):
                        publication[key] = str(value)

            return jsonify(publications)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_publications_conference', methods=['GET'])
def get_publications_conference():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, scsswsg, authors_designation, conference_name, paper_title, issn, doi, volume, page, month_year
                FROM conference_publications
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            publications = cursor.fetchall()

            # Convert non-serializable objects to strings
            for publication in publications:
                for key, value in publication.items():
                    if isinstance(value, timedelta):
                        publication[key] = str(value)

            return jsonify(publications)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_workshops', methods=['GET'])
def get_workshops():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, event_name, national_international, event_type, event_date, organized_by
                FROM workshop_attendance
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            workshops = cursor.fetchall()

            # Convert non-serializable objects to strings
            for workshop in workshops:
                for key, value in workshop.items():
                    if isinstance(value, timedelta):
                        workshop[key] = str(value)

            return jsonify(workshops)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_achievements', methods=['GET'])
def get_achievements():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, achievement_name, awarded_by, achievement_date
                FROM student_achievements
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            achievements = cursor.fetchall()

            # Convert non-serializable objects to strings
            for achievement in achievements:
                for key, value in achievement.items():
                    if isinstance(value, timedelta):
                        achievement[key] = str(value)

            return jsonify(achievements)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_industry_visits', methods=['GET'])
def get_industry_visits():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, industry_name, visit_date, significance, location
                FROM industry_visits
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            visits = cursor.fetchall()

            # Convert non-serializable objects to strings
            for visit in visits:
                for key, value in visit.items():
                    if isinstance(value, timedelta):
                        visit[key] = str(value)

            return jsonify(visits)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_vedic_workshops', methods=['GET'])
def get_vedic_workshops():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, workshop_name, event_date, venue
                FROM vedic_workshops
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            workshops = cursor.fetchall()

            # Convert non-serializable objects to strings
            for workshop in workshops:
                for key, value in workshop.items():
                    if isinstance(value, timedelta):
                        workshop[key] = str(value)

            return jsonify(workshops)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_outside_competitions', methods=['GET'])
def get_outside_competitions():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, competition_name, organized_by, duration, level
                FROM outside_competitions
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            competitions = cursor.fetchall()

            # Convert non-serializable objects to strings
            for competition in competitions:
                for key, value in competition.items():
                    if isinstance(value, timedelta):
                        competition[key] = str(value)

            return jsonify(competitions)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_sports_participation', methods=['GET'])
def get_sports_participation():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, year, game_name, game_details, organized_by, venue, event_start_date, event_end_date, secured_position, level
                FROM sports_participation
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            sports = cursor.fetchall()

            # Convert non-serializable objects to strings
            for sport in sports:
                for key, value in sport.items():
                    if isinstance(value, timedelta):
                        sport[key] = str(value)

            return jsonify(sports)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_certifications', methods=['GET'])
def get_certifications():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, course_title, duration, course_topic, details, certificate_path
                FROM certifications
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            certifications = cursor.fetchall()

            # Convert non-serializable objects to strings
            for certification in certifications:
                for key, value in certification.items():
                    if isinstance(value, timedelta):
                        certification[key] = str(value)

            return jsonify(certifications)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/get_nptel_courses', methods=['GET'])
def get_nptel_courses():
    registration_number = request.args.get('registration_number')
    if not registration_number:
        registration_number = session.get('user_id')
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT student_name, registration_number, department, course_title, duration, course_id, score, platform, details, certificate_path
                FROM nptel_courses
                WHERE registration_number = %s
            """
            cursor.execute(query, (registration_number,))
            courses = cursor.fetchall()

            # Convert non-serializable objects to strings
            for course in courses:
                for key, value in course.items():
                    if isinstance(value, timedelta):
                        course[key] = str(value)

            return jsonify(courses)
        except mysql.connector.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'Failed to connect to database'}), 500


@app.route('/submit_patent', methods=['POST'])
def submit_patent():
    if request.method == 'POST':
        try:
            applicant_name = request.form['Applicant']
            inventors = request.form['studentpatentinventorName']
            department = request.form['department']
            patent_title = request.form['Studentpatenttitle']
            patent_number = request.form['studentpatentnumber']
            status = ', '.join(request.form.getlist('sfpg'))
            filed_date = request.form['studentpatentfileddate']
            published_date = request.form['studentpatentpublisheddate']
            granted_date = request.form['studentpatentgranteddate']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO patents (applicant_name, inventors, department, patent_title, patent_number, status, filed_date, published_date, granted_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (applicant_name, inventors, department, patent_title, patent_number, status, filed_date, published_date, granted_date))
            conn.commit()
            flash('Patent data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))

@app.route('/submit_publication_journals', methods=['POST'])
def submit_publication():
    if request.method == 'POST':
        try:
            student_name = request.form['journalstudentname']
            registration_number = request.form['journalstudentRegistratioNumber']
            department = request.form['departmenT']
            journal_type = request.form['sjsswsg']
            authors = request.form['studentjournalsAuthorsDesignation']
            journal_name = request.form['studentjournalname']
            paper_title = request.form['studentjournalpapertitle']
            issn = request.form['studentjournalissn']
            quartile_ranking = request.form['studentjournalQuartileRanking']
            doi = request.form['studentjournaldoi']
            volume = request.form['studentjournalvolume']
            page = request.form['studentjournalpage']
            month_year = request.form['studentjournalmonthandyear']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO publications (student_name, registration_number, department, journal_type, authors, journal_name, paper_title, issn, quartile_ranking, doi, volume, page, month_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, journal_type, authors, journal_name, paper_title, issn, quartile_ranking, doi, volume, page, month_year))
            conn.commit()
            flash('Publication data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_publications_conference', methods=['POST'])
def submit_publication_conference():
    if request.method == 'POST':
        try:
            student_name = request.form['conferencestudentname']
            registration_number = request.form['conferencestudentRegistratioNumber']
            department = request.form['departmeNt']
            scsswsg = request.form['scsswsg']
            authors_designation = request.form['studentconferenceauthorsdesignation']
            conference_name = request.form['studentconferencename']
            paper_title = request.form['studentconferencepapertitle']
            issn = request.form['studentconferenceissn']
            doi = request.form['studentconferencedoi']
            volume = request.form['studentconferencevolume']
            page = request.form['studentconferencepage']
            month_year = request.form['studentconferencemonthandyear']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO conference_publications (student_name, registration_number, department, scsswsg, authors_designation, conference_name, paper_title, issn, doi, volume, page, month_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, scsswsg, authors_designation, conference_name, paper_title, issn, doi, volume, page, month_year))
            conn.commit()
            flash('Conference publication data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_workshop', methods=['POST'])
def submit_workshop():
    if request.method == 'POST':
        student_name = request.form['workshopattendedstudentname']
        registration_number = request.form['workshopattendedRegistratioNumber']
        department = request.form['departmEnt']
        event_name = request.form['studentattendedworkshopname']
        national_international = request.form['studentattendedworkshopNIn']
        event_type = request.form['studentattendedwgstype']
        event_date = request.form['studentattendedWSDate']
        organized_by = request.form['studentattendedwsorganisedby']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO workshop_attendance (student_name, registration_number, department, event_name, national_international, event_type, event_date, organized_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, event_name, national_international, event_type, event_date, organized_by))
            conn.commit()
            flash('Workshop/Seminar/Guest Lecture data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_achievement', methods=['POST'])
def submit_achievement():
    if request.method == 'POST':
        try:
            student_name = request.form['acheivementawardedstudentname']
            registration_number = request.form['acheivementawardedstudentRegistratioNumber']
            department = request.form['DepartMent']
            achievement_name = request.form['studentacheivementname']
            awarded_by = request.form['studentacheivementAwardedby']
            achievement_date = request.form['studentacheivementmonthandyear']  # Directly store as VARCHAR
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO student_achievements (student_name, registration_number, department, achievement_name, awarded_by, achievement_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, achievement_name, awarded_by, achievement_date))
            conn.commit()
            flash('Achievement data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_industry_visit', methods=['POST'])
def submit_industry_visit():
    if request.method == 'POST':
        try:
            student_name = request.form['industryvisitedstudentname']
            registration_number = request.form['industryvisitedstudentRegistratioNumber']
            department = request.form['deparTment']
            industry_name = request.form['studentvisitedindustryname']
            visit_date = request.form['studentvisitedindustryDate']  # Date will be received as 'YYYY-MM-DD'
            significance = request.form['studentvisitedindustrySignificance']
            location = request.form['studentvisitedindustrylocation']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO industry_visits (student_name, registration_number, department, industry_name, visit_date, significance, location)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, industry_name, visit_date, significance, location))
            conn.commit()
            flash('Industry visit data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_vedic_workshop', methods=['POST'])
def submit_vedic_workshop():
    if request.method == 'POST':
        try:
            student_name = request.form['vedicattendedstudentname']
            registration_number = request.form['vedicattendedstudentRegistrationNumber']
            department = request.form['depaRtment']
            workshop_name = request.form['studentattendedvedicworkshopname']
            event_date = request.form['studentattendedvedicworkshopdate']  # Date will be received as 'YYYY-MM-DD'
            venue = request.form['studentattendedvedicvenue']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO vedic_workshops (student_name, registration_number, department, workshop_name, event_date, venue)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, workshop_name, event_date, venue))
            conn.commit()
            flash('VEDIC workshop data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_outside_competition', methods=['POST'])
def submit_outside_competition():
    if request.method == 'POST':
        try:
            student_name = request.form['outsideparicipatedstudentname']
            registration_number = request.form['outsideparicipatedstudentRegistrationNumber']
            department = request.form['depArtmeNt']
            competition_name = request.form['studentattendedNameoftheWSP']
            organized_by = request.form['studentattendedparticipationOrganisedbY']
            duration = request.form['studentattendedparticipationduration']
            level = request.form['studentattendedparticipationNaIn']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO outside_competitions (student_name, registration_number, department, competition_name, organized_by, duration, level)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, competition_name, organized_by, duration, level))
            conn.commit()
            flash('Competition participation data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
@app.route('/submit_sports_participation', methods=['POST'])
def submit_sports_participation():
    if request.method == 'POST':
        try:
            student_name = request.form['sportparticipatedstudentname']
            registration_number = request.form['sportparticipatedstudentRegistratioNumber']
            department = request.form['dePartment']
            year = request.form['sportparticipatedstudentyear']
            game_name = request.form['NameoftheGameparticipated']
            game_details = request.form['participatedGameDetails']
            organized_by = request.form['participatedgameOrganisedBY']
            venue = request.form['participatedgamevenue']
            event_start_date = request.form['gameeventstartingdate']
            event_end_date = request.form['gameeventendingdate']
            secured_position = request.form['gameSecuredPosition']
            level = request.form['gameNaIna']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO sports_participation (student_name, registration_number, department, year, game_name, game_details, organized_by, venue, event_start_date, event_end_date, secured_position, level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, year, game_name, game_details, organized_by, venue, event_start_date, event_end_date, secured_position, level))
            conn.commit()
            flash('Sports participation data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4'))
    
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/submit_certifications', methods=['POST'])
def submit_certifications():
    if request.method == 'POST':
        student_name = request.form['certificatedstudentname']
        registration_number = request.form['certificatedstudentRegistrationNumber']
        department = request.form['dEpartment']
        course_title = request.form['studentcertificatedCourseTitle']
        duration = request.form['studentcertificatedCourseduration']
        course_topic = request.form['studentcertificatedCourseTopic']
        details = request.form['studentcertifiatedcoursedetails']

        # Handling file upload
        file = request.files['studentcertificationsUpload']
        certificate_path = None
        if file and file.filename:
            certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(certificate_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO certifications (student_name, registration_number, department, course_title, duration, course_topic, details, certificate_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, course_title, duration, course_topic, details, certificate_path))
            conn.commit()
            flash('Certification data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4'))
    
@app.route('/submit_nptel_courses', methods=['POST'])
def submit_nptel_courses():
    if request.method == 'POST':
        student_name = request.form.get('nptelstudentname')
        registration_number = request.form.get('nptelstudentRegistrationNumber')
        department = request.form.get('Department')
        course_title = request.form.get('nptelstudentCourseTitle')
        duration = request.form.get('nptelstudentCourseduration')
        course_id = request.form.get('nptelstudentcourseid')
        score = request.form.get('nptelstudentScore')
        platform = request.form.get('studentcourseplatform')
        details = request.form.get('studentcoursedeTails')

        # Handling file upload safely
        certificate_path = None
        if 'studentsnptelUpload' in request.files:
            file = request.files['studentsnptelUpload']
            if file and file.filename:
                certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(certificate_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO nptel_courses (student_name, registration_number, department, course_title, duration, course_id, score, platform, details, certificate_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, registration_number, department, course_title, duration, course_id, score, platform, details, certificate_path))
            conn.commit()
            flash('NPTEL / Online Course data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4'))
    
@app.route('/login6', methods=['POST'])
def login6():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE faculty SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500
    
@app.route('/get_faculty_patents', methods=['GET'])
def get_faculty_patents():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT faculty_id, applicant_name, inventors, department, patent_title, patent_number, status, filed_date, published_date, granted_date
            FROM faculty_patents
            WHERE department = %s
        '''
        params = [department]
        if faculty:
            query += ' AND (faculty_id = %s OR applicant_name = %s)'
            params.extend([faculty, faculty])
        if year:
            query += ' AND (YEAR(filed_date) = %s OR YEAR(published_date) = %s OR YEAR(granted_date) = %s)'
            params.extend([year, year, year])
        if month:
            query += ' AND (MONTH(filed_date) = %s OR MONTH(published_date) = %s OR MONTH(granted_date) = %s)'
            params.extend([month, month, month])
        cursor.execute(query, tuple(params))
        patents = cursor.fetchall()
        return jsonify(patents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_research_grants', methods=['GET'])
def get_research_grants():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, project_id, project_title, funding_agency,
                   principle_investigator, co_pi, project_duration, total_grant_sanctioned
            FROM research_grants
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND (faculty_id = %s OR faculty_name = %s)'
            params.extend([faculty, faculty])
        if year:
            query += ' AND (YEAR(project_duration) = %s)'
            params.append(year)
        if month:
            query += ' AND (MONTH(project_duration) = %s)'
            params.append(month)
        cursor.execute(query, tuple(params))
        grants = cursor.fetchall()
        for grant in grants:
            for key, value in grant.items():
                if isinstance(value, timedelta):
                    grant[key] = str(value)
        return jsonify(grants)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_consultancy', methods=['GET'])
def get_consultancy():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, consultancy_name, department, funding_agency, faculty_names, duration, amount_granted
            FROM consultancy
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND (faculty_id = %s OR faculty_name = %s OR faculty_names LIKE %s)'
            params.extend([faculty, faculty, f'%{faculty}%'])
        if year:
            query += ' AND (YEAR(duration) = %s)'
            params.append(year)
        if month:
            query += ' AND (MONTH(duration) = %s)'
            params.append(month)
        cursor.execute(query, tuple(params))
        consultancy_data = cursor.fetchall()
        for consultancy in consultancy_data:
            for key, value in consultancy.items():
                if isinstance(value, timedelta):
                    consultancy[key] = str(value)
        return jsonify(consultancy_data)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_journals', methods=['GET'])
def get_faculty_journals():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, journal_type, authors_designations, journal_name,
                   paper_title, issn, quartile_ranking, doi, volume, page, month_and_year
            FROM faculty_journals
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND (faculty_id = %s OR faculty_name = %s)'
            params.extend([faculty, faculty])
        if year:
            query += ' AND (YEAR(month_and_year) = %s OR month_and_year LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(month_and_year) = %s OR month_and_year LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        journals = cursor.fetchall()
        for journal in journals:
            for key, value in journal.items():
                if isinstance(value, timedelta):
                    journal[key] = str(value)
        return jsonify(journals)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_conferences', methods=['GET'])
def get_faculty_conferences():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, conference_type, authors_designations, conference_name,
                   paper_title, issn, doi, volume, page, month_and_year
            FROM faculty_conferences
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND (faculty_id = %s OR faculty_name = %s)'
            params.extend([faculty, faculty])
        if year:
            query += ' AND (YEAR(month_and_year) = %s OR month_and_year LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(month_and_year) = %s OR month_and_year LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        conferences = cursor.fetchall()
        for conference in conferences:
            for key, value in conference.items():
                if isinstance(value, timedelta):
                    conference[key] = str(value)
        return jsonify(conferences)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_resource_person', methods=['GET'])
def get_faculty_resource_person():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, date_of_activity, college_name, resource_activity, remarks
            FROM faculty_resource_person
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND YEAR(date_of_activity) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(date_of_activity) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        resource_persons = cursor.fetchall()
        for resource_person in resource_persons:
            for key, value in resource_person.items():
                if isinstance(value, timedelta):
                    resource_person[key] = str(value)
        return jsonify(resource_persons)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_book_publications', methods=['GET'])
def get_book_publications():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, designation, department, book_type, book_title, isbn, indexed_in, publishing_agency, month_and_year
            FROM faculty_books
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(month_and_year) = %s OR month_and_year LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(month_and_year) = %s OR month_and_year LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        book_publications = cursor.fetchall()
        for book_publication in book_publications:
            for key, value in book_publication.items():
                if isinstance(value, timedelta):
                    book_publication[key] = str(value)
        return jsonify(book_publications)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_industry_visits', methods=['GET'])
def get_faculty_industry_visits():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, industry_name, visit_date, significance, location
            FROM faculty_industry_visits
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND YEAR(visit_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(visit_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        industry_visits = cursor.fetchall()
        for industry_visit in industry_visits:
            for key, value in industry_visit.items():
                if isinstance(value, timedelta):
                    industry_visit[key] = str(value)
        return jsonify(industry_visits)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_hrd_fdp_sdp', methods=['GET'])
def get_faculty_hrd_fdp_sdp():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, program_name, program_type, start_date,
                   end_date, organized_by, national_international, mode
            FROM faculty_hrd_fdp_sdp
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(start_date) = %s OR YEAR(end_date) = %s)'
            params.extend([year, year])
        if month:
            query += ' AND (MONTH(start_date) = %s OR MONTH(end_date) = %s)'
            params.extend([month, month])
        cursor.execute(query, tuple(params))
        hrd_fdp_sdp = cursor.fetchall()
        for hrd in hrd_fdp_sdp:
            for key, value in hrd.items():
                if isinstance(value, timedelta):
                    hrd[key] = str(value)
        return jsonify(hrd_fdp_sdp)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_ws_sem_gs', methods=['GET'])
def get_faculty_ws_sem_gs():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, event_name, national_international, event_type,
                   start_date, end_date, organized_by
            FROM faculty_ws_sem_gs
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(start_date) = %s OR YEAR(end_date) = %s)'
            params.extend([year, year])
        if month:
            query += ' AND (MONTH(start_date) = %s OR MONTH(end_date) = %s)'
            params.extend([month, month])
        cursor.execute(query, tuple(params))
        ws_sem_gs = cursor.fetchall()
        for ws in ws_sem_gs:
            for key, value in ws.items():
                if isinstance(value, timedelta):
                    ws[key] = str(value)
        return jsonify(ws_sem_gs)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_achievements', methods=['GET'])
def get_faculty_achievements():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, achievement_name, awarded_by, month_and_year
            FROM faculty_achievements
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(month_and_year) = %s OR month_and_year LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(month_and_year) = %s OR month_and_year LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        achievements = cursor.fetchall()
        for achievement in achievements:
            for key, value in achievement.items():
                if isinstance(value, timedelta):
                    achievement[key] = str(value)
        return jsonify(achievements)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_vedic_workshops', methods=['GET'])
def get_faculty_vedic_workshops():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, workshop_name, event_date, venue
            FROM faculty_vedic_workshops
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND YEAR(event_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(event_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        vedic_workshops = cursor.fetchall()
        for workshop in vedic_workshops:
            for key, value in workshop.items():
                if isinstance(value, timedelta):
                    workshop[key] = str(value)
        return jsonify(vedic_workshops)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_phd_supervisor_details', methods=['GET'])
def get_phd_supervisor_details():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT supervisor_name, research_scholar_name, department, university_name,
                   full_time_part_time, month_year_of_joining, status
            FROM phd_supervisor_details
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND supervisor_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(month_year_of_joining) = %s OR month_year_of_joining LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(month_year_of_joining) = %s OR month_year_of_joining LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        phd_supervisors = cursor.fetchall()
        for supervisor in phd_supervisors:
            for key, value in supervisor.items():
                if isinstance(value, timedelta):
                    supervisor[key] = str(value)
        return jsonify(phd_supervisors)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_conference_journal_reviewer', methods=['GET'])
def get_conference_journal_reviewer():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, date_of_review, conference_journal_name, review_type, remarks
            FROM conference_journal_reviewer
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND YEAR(date_of_review) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(date_of_review) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        reviewer_data = cursor.fetchall()
        for reviewer in reviewer_data:
            for key, value in reviewer.items():
                if isinstance(value, timedelta):
                    reviewer[key] = str(value)
        return jsonify(reviewer_data)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_certifications', methods=['GET'])
def get_faculty_certifications():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, course_title, course_duration,
                   course_topic, course_details, certificate_path
            FROM faculty_certifications
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(course_duration) = %s OR course_duration LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(course_duration) = %s OR course_duration LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        certifications = cursor.fetchall()
        for certification in certifications:
            for key, value in certification.items():
                if isinstance(value, timedelta):
                    certification[key] = str(value)
        return jsonify(certifications)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_faculty_nptel_courses', methods=['GET'])
def get_faculty_nptel_courses():
    department = request.args.get('department')
    faculty = request.args.get('faculty')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT faculty_id, faculty_name, department, course_title, course_duration,
                   course_id, score, platform, details, certificate_path
            FROM faculty_nptel_courses
            WHERE department = %s
        """
        params = [department]
        if faculty:
            query += ' AND faculty_name = %s'
            params.append(faculty)
        if year:
            query += ' AND (YEAR(course_duration) = %s OR course_duration LIKE %s)'
            params.extend([year, f'%{year}%'])
        if month:
            query += ' AND (MONTH(course_duration) = %s OR course_duration LIKE %s)'
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            month_name = month_names[int(month) - 1] if month.isdigit() and 1 <= int(month) <= 12 else month
            params.extend([month, f'%{month_name}%'])
        cursor.execute(query, tuple(params))
        nptel_courses = cursor.fetchall()
        for course in nptel_courses:
            for key, value in course.items():
                if isinstance(value, timedelta):
                    course[key] = str(value)
        return jsonify(nptel_courses)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route('/submit_faculty_patents', methods=['POST'])
@app.route('/submit_faculty_patent', methods=['POST'])
def submit_faculty_patent():
    if request.method == 'POST':
        try:
            inventors = request.form['facultypatentapplicant']
            department = request.form['DEPARTMENT']
            faculty_id = request.form.get('faculty_id_3')
            applicant_name = request.form['faculty_name_3']  # auto-filled
            patent_title = request.form['facultypatenttitle']
            patent_number = request.form['facultypatentnumber']
            status = ', '.join(request.form.getlist('ffpg'))
            filed_date = request.form.get('facultypatentfileddate') or None
            published_date = request.form.get('facultypatentpublisheddate') or None
            granted_date = request.form.get('facultypatentgranteddate') or None
            if not applicant_name:
                flash('Faculty Name is required!', 'danger')
                return redirect(url_for('page4_faculty'))
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO faculty_patents (faculty_id, applicant_name, inventors, department, patent_title, patent_number, status, filed_date, published_date, granted_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (faculty_id, applicant_name, inventors, department, patent_title, patent_number, status, filed_date, published_date, granted_date))
            conn.commit()
            flash('Patent data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Database Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_research_grant', methods=['POST'])
def submit_research_grant():
    if request.method == 'POST':
        # Extract form data
        faculty_id = request.form.get('faculty_id_2')
        faculty_name = request.form.get('faculty_name_2')  # auto-filled
        department = request.form['DEPARTMENt']
        project_id = request.form['ProjectID']
        project_title = request.form['Projecttitle']
        funding_agency = request.form['researchagency']
        principle_investigator = request.form['Principleinvestigator']
        co_pi = request.form['researchCOPI']
        project_duration = request.form['researchprojectduration']
        total_grant_sanctioned = request.form['researchTGS']

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO research_grants (
                    faculty_id, faculty_name, department, project_id, project_title, funding_agency,
                    principle_investigator, co_pi, project_duration, total_grant_sanctioned
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, project_id, project_title, funding_agency,
                principle_investigator, co_pi, project_duration, total_grant_sanctioned
            ))
            conn.commit()
            flash('Research grant data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_consultancy', methods=['POST'])
def submit_consultancy():
    if request.method == 'POST':
        try:
            consultancy_name = request.form['Consultancyname']
            department = request.form['DEPARTMEnT']
            faculty_id = request.form.get('faculty_id_3')
            faculty_name = request.form['faculty_name_3']  # auto-filled
            funding_agency = request.form['consultancyagency']
            faculty_names = request.form['consultancyfaculty']
            duration = request.form['consultancyduration']
            amount_granted = request.form['consultancyamountgranted']
            if not faculty_name:
                flash('Faculty Name is required!', 'danger')
                return redirect(url_for('page4_faculty'))
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO consultancy (
                    faculty_id, consultancy_name, department, faculty_name, funding_agency, faculty_names, duration, amount_granted
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, consultancy_name, department, faculty_name, funding_agency, faculty_names, duration, amount_granted
            ))
            conn.commit()
            flash('Consultancy data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            error_details = f"Consultancyname: {consultancy_name}, DEPARTMEnT: {department}, faculty_name_3: {faculty_name}, consultancyagency: {funding_agency}, consultancyfaculty: {faculty_names}, consultancyduration: {duration}, consultancyamountgranted: {amount_granted}"
            flash(f'Database Error: {str(e)} | Submitted values: {error_details}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_journals', methods=['POST'])
def submit_faculty_journals():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_4')
            faculty_name = request.form.get('faculty_name_4')  # auto-filled
            department = request.form['DEPARTMeNT']
            journal_type = request.form['fjSSWS']
            authors_designations = request.form['facultyjournalAuthorsDesign']
            journal_name = request.form['facultyjournalname']
            paper_title = request.form['facultyjurnalpapertitle']
            issn = request.form['facultyjournalissn']
            quartile_ranking = request.form['facultyjournalQuartileRanking']
            doi = request.form['facultyjournaldoi']
            volume = request.form['facultyjournalvolume']
            page = request.form['facultyjournalpage']
            month_and_year = request.form['facultyjournalmonthandyear']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_journals (
                    faculty_id, faculty_name, department, journal_type, authors_designations, journal_name,
                    paper_title, issn, quartile_ranking, doi, volume, page, month_and_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, journal_type, authors_designations, journal_name,
                paper_title, issn, quartile_ranking, doi, volume, page, month_and_year
            ))
            conn.commit()
            flash('Faculty journal data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_conference', methods=['POST'])
def submit_faculty_conference():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_5')
            faculty_name = request.form.get('faculty_name_5')  # auto-filled
            department = request.form['DEPARTmENT']
            conference_type = request.form['fcssws']
            authors_designations = request.form['facultyconferenceAuthorsDsgn']
            conference_name = request.form['facultyconferencename']
            paper_title = request.form['facultyconferencetitlename']
            issn = request.form['facultyconferenceissn']
            doi = request.form['facultyconferencedoi']
            volume = request.form['facultyconferencevolume']
            page = request.form['facultyconferencepage']
            month_and_year = request.form['facultyconferencemonth']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_conferences (
                    faculty_id, faculty_name, department, conference_type, authors_designations, conference_name,
                    paper_title, issn, doi, volume, page, month_and_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, conference_type, authors_designations, conference_name,
                paper_title, issn, doi, volume, page, month_and_year
            ))
            conn.commit()
            flash('Faculty conference data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_acted_resourveperson', methods=['POST'])
def submit_faculty_acted_resourceperson():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_6')
            faculty_name = request.form['faculty_name_6']
            department = request.form['DEPARtMENT']
            date_of_activity = request.form['Dateoffacultyresourceactivity']
            college_name = request.form['facultyresourcecollege']
            resource_activity = request.form['facultyResourceActivity']
            remarks = request.form['facultyresourceactivityremaarks']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_resource_person (
                    faculty_id, faculty_name, department, date_of_activity, college_name, resource_activity, remarks
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, date_of_activity, college_name, resource_activity, remarks
            ))
            conn.commit()
            flash('Faculty resource person data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_book_publications', methods=['POST'])
def submit_book_publications():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_7')
            faculty_name = request.form['faculty_name_7']
            designation = request.form['bookpublishedfacultydesignation']
            department = request.form['DEPArTMENT']
            book_type = request.form['fbssws']
            book_title = request.form['facultypublishedbooktitle']
            isbn = request.form['facultypublishedbookisbn']
            indexed_in = request.form['facultybookindexedin']
            publishing_agency = request.form['facultybookpublishingagency']
            month_and_year = request.form['facultybookpublishedmonthandyear']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_books (
                    faculty_id, faculty_name, designation, department, book_type, book_title,
                    isbn, indexed_in, publishing_agency, month_and_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, designation, department, book_type, book_title,
                isbn, indexed_in, publishing_agency, month_and_year
            ))
            conn.commit()
            flash('Book publication data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_industry_visits', methods=['POST'])
def submit_faculty_industry_visits():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_8')
            faculty_name = request.form['faculty_name_8']
            department = request.form['DEPaRTMENT']
            industry_name = request.form['nameofindustryfacultyvisited']
            visit_date = request.form['facultyindustryVistedDate']
            significance = request.form['facultyindustrialvisitSignificance']
            location = request.form['facultyvisitedindustrylocation']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_industry_visits (
                    faculty_id, faculty_name, department, industry_name, visit_date, significance, location
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, industry_name, visit_date, significance, location
            ))
            conn.commit()
            flash('Faculty industry visit data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_hrd_fdp_sdp', methods=['POST'])
def submit_faculty_hrd_fdp_sdp():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_9')
            faculty_name = request.form['faculty_name_9']
            department = request.form['DEpARTMENT']
            program_name = request.form['facultyattendedhrdname']
            program_type = request.form['facultyhrdattendedtype']
            start_date = request.form['facultyattendedStartingFDPHRDDate']
            end_date = request.form['facultyattendedEndingFDPHRDDate']
            organized_by = request.form['facultyattendehrdorganisedby']
            national_international = request.form['facultyattendedhrdNIn']
            mode = request.form['facultyattendedHRDmode']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_hrd_fdp_sdp (
                    faculty_id, faculty_name, department, program_name, program_type, start_date,
                    end_date, organized_by, national_international, mode
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, program_name, program_type, start_date,
                end_date, organized_by, national_international, mode
            ))
            conn.commit()
            flash('Faculty HRD/FDP/SDP data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_ws_sem_gs', methods=['POST'])
def submit_faculty_ws_sem_gs():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_10')
            faculty_name = request.form['faculty_name_10']
            department = request.form['DePARTMENT']
            event_name = request.form['facultyattendedwsname']
            national_international = request.form['facultyattendedwsNIn']
            event_type = request.form['facultyattendedwgs']
            start_date = request.form['facultyattendedStartingWSDate']
            end_date = request.form['facultyattendedEndingWSDDate']
            organized_by = request.form['facultyattendedwsorganisedby']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))
        
        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_ws_sem_gs (
                    faculty_id, faculty_name, department, event_name, national_international, event_type,
                    start_date, end_date, organized_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, event_name, national_international, event_type,
                start_date, end_date, organized_by
            ))
            conn.commit()
            flash('Faculty workshop/seminar/guest lecture data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_acheivements', methods=['POST'])
def submit_faculty_achievements():
    if request.method == 'POST':
        # Extract form data
        try:
            faculty_id = request.form.get('faculty_id_11')
            faculty_name = request.form['faculty_name_11']
            department = request.form['dEPARTMENT']
            achievement_name = request.form['facultyAcheivementname']
            awarded_by = request.form['facultyacheivemntAwardedby']
            month_and_year = request.form['facultyawardedmonthandyear']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4-faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_achievements (
                    faculty_id, faculty_name, department, achievement_name, awarded_by, month_and_year
                ) VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, achievement_name, awarded_by, month_and_year
            ))
            conn.commit()
            flash('Faculty achievement data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_vedic', methods=['POST'])
def submit_faculty_vedic():
    if request.method == 'POST':
        try:
            faculty_id = request.form.get('faculty_id_12')
            faculty_name = request.form['faculty_name_12']  # auto-filled
            department = request.form['DEPT']
            workshop_name = request.form['facultyattendedvedicworkshopname']
            event_date = request.form['facultyattendedvedicwsname']
            venue = request.form['facultyattendedvedicvenue']
            if not faculty_name:
                flash('Faculty Name is required!', 'danger')
                return redirect(url_for('page4_faculty'))
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO faculty_vedic_workshops (
                    faculty_id, faculty_name, department, workshop_name, event_date, venue
                ) VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, workshop_name, event_date, venue
            ))
            conn.commit()
            flash('Faculty VEDIC workshop data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            error_details = f"faculty_name_12: {faculty_name}, DEPT: {department}, facultyattendedvedicworkshopname: {workshop_name}, facultyattendedvedicwsname: {event_date}, facultyattendedvedicvenue: {venue}"
            flash(f'Database Error: {str(e)} | Submitted values: {error_details}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_phd_supervisor', methods=['POST'])
def submit_phd_supervisor():
    if request.method == 'POST':
        # Extract form data
        try:
            supervisor_name = request.form['Supervisorname']
            research_scholar_name = request.form['NameoftheResearchScholar']
            department = request.form['DEPt']
            university_name = request.form['phdscholarUniversityName']
            full_time_part_time = request.form['phdFtPt']
            month_year_of_joining = request.form['phdMonthyearofJoining']
            status = request.form['phdStatus']
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
            return redirect(url_for('page4_faculty'))

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO phd_supervisor_details (
                    supervisor_name, research_scholar_name, department, university_name,
                    full_time_part_time, month_year_of_joining, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                supervisor_name, research_scholar_name, department, university_name,
                full_time_part_time, month_year_of_joining, status
            ))
            conn.commit()
            flash('Ph.D supervisor details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_conference_journal_reviewer', methods=['POST'])
def submit_conference_journal_reviewer():
    if request.method == 'POST':
        try:
            # Extract form data
            faculty_id = request.form.get('faculty_id_14')
            faculty_name = request.form.get('faculty_name_14')  # auto-filled
            department = request.form['DEpT']
            date_of_review = request.form['Dateofattenedasreviewer']
            conference_journal_name = request.form['reviewattendedCollegename']
            review_type = request.form['reviewtypeConferenceJournal']
            remarks = request.form['facultyattendedreviewremarks']

            # Get a database connection from the pool
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Insert data into the database
                cursor.execute('''
                    INSERT INTO conference_journal_reviewer (
                        faculty_id, faculty_name, department, date_of_review, conference_journal_name, review_type, remarks
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    faculty_id, faculty_name, department, date_of_review, conference_journal_name, review_type, remarks
                ))
                conn.commit()
                flash('Conference/Journal Reviewer data submitted successfully!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                conn.close()
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'danger')
        return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_certifications', methods=['POST'])
def submit_faculty_certifications():
    if request.method == 'POST':
        # Extract form data
        faculty_id = request.form.get('faculty_id_15')
        faculty_name = request.form.get('faculty_name_15')  # auto-filled
        department = request.form['DePT']
        course_title = request.form['facultycertificatedCourseTitle']
        course_duration = request.form['facultycertificatedcourseduration']
        course_topic = request.form['facultycertificatedCourseTopic']
        course_details = request.form['facultycertificatedcoursedetails']
        file = request.files["facultycertificationsUpload"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        print(f"Received: {faculty_name}, {department}, {course_title}, {course_duration}, {course_topic}, {course_details}, {file_path}")
        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main rd_events table
            cursor.execute('''
                INSERT INTO faculty_certifications (
                    faculty_id, faculty_name, department, course_title, course_duration,
                    course_topic, course_details, certificate_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, course_title, course_duration,
                course_topic, course_details, file_path
            ))
            conn.commit()
            print(file_path)
            flash('R&D Event details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('page4_faculty'))
    
@app.route('/submit_faculty_nptel', methods=['POST'])
def submit_faculty_nptel():
    if request.method == 'POST':
        # Extract form data
        faculty_id = request.form.get('faculty_id_16')
        faculty_name = request.form['faculty_name_16']
        department = request.form['dEPT']
        course_title = request.form['facultynptelCourseTitle']
        course_duration = request.form['facultynptelcourseduration']
        course_id = request.form.get('facultynptelcourseID', '')  # Optional field
        score = request.form.get('facultynptelScore', '')  # Optional field
        platform = request.form['facultynptelplatform']
        details = request.form['facultynpteldetails']

        # Handle file upload
        file = request.files["facultynptelUpload"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Debugging: Print received form data
        print(f"Received: {faculty_name}, {department}, {course_title}, {course_duration}, {course_id}, {score}, {platform}, {details}, {file_path}")

        # Get a database connection from the pool
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert data into the database
            cursor.execute('''
                INSERT INTO faculty_nptel_courses (
                    faculty_id, faculty_name, department, course_title, course_duration,
                    course_id, score, platform, details, certificate_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                faculty_id, faculty_name, department, course_title, course_duration,
                course_id, score, platform, details, file_path
            ))
            conn.commit()
            flash('NPTEL/Online course data submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_faculty'))

@app.route('/login7', methods=['POST'])
def login7():
    userid = request.form['userid']
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update password if old password matches
            query = "UPDATE dept SET password = %s WHERE user_id = %s AND password = %s"
            cursor.execute(query, (newpassword, userid, oldpassword))
            conn.commit()  # Commit the transaction

            if cursor.rowcount > 0:
                return "Password changed successfully", 200
            else:
                return "Invalid credentials or no changes made", 401

        except Error as e:
            return f"Database Error: {e}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Unable to connect to database", 500
    
@app.route('/get_laboratories', methods=['GET'])
def get_laboratories():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT id, lab_name, department, equipment_name, quantity, cost, 
                   purchase_date, company_name, specifications, remarks
            FROM laboratory_purchases
        '''
        
        if department:
            query += " WHERE department = %s"
            cursor.execute(query, (department,))
        else:
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Student Chapters
@app.route('/get_student_chapters', methods=['GET'])
def get_student_chapters():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT sc.id, sc.event_name, sc.start_date, sc.end_date, sc.venue, 
                   sc.resource_person, sc.college, sc.participant_count, sc.details,
                   GROUP_CONCAT(ed.department SEPARATOR ', ') AS departments
            FROM student_chapters sc
            LEFT JOIN student_chapter_departments ed ON sc.id = ed.chapter_id
        '''
        
        if department:
            query += " WHERE ed.department = %s"
            query += " GROUP BY sc.id"
            cursor.execute(query, (department,))
        else:
            query += " GROUP BY sc.id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Higher Education
@app.route('/get_higher_education', methods=['GET'])
def get_higher_education():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT id, student_name, register_number, department, exam_type, 
                   exam_rank, exam_score, course, admitted_college, location, remarks
            FROM higher_education
        '''
        
        if department:
            query += " WHERE department = %s"
            cursor.execute(query, (department,))
        else:
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Internship Opportunities
@app.route('/get_internships', methods=['GET'])
def get_internships():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT id, student_name, register_number, department, allowed_year, 
                   company_name, company_details, start_date, end_date, duration, 
                   designation, stipend, mode, location, remarks
            FROM internship_opportunities
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("department = %s")
            params.append(department)
        if year:
            conditions.append("allowed_year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Alumni Cell
@app.route('/get_alumni', methods=['GET'])
def get_alumni():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT id, alumni_name, talk_title, event_date, beneficiaries, 
                   alumni_job, alumni_regdno, company_details, department, 
                   participants, remarks
            FROM alumni_cell
        '''
        
        if department:
            query += " WHERE department = %s"
            cursor.execute(query, (department,))
        else:
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# MOU Academia
@app.route('/get_mous', methods=['GET'])
def get_mous():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT id, university, contact_person, designation, start_date, 
                   end_date, mou_period, purpose, file_path, remarks
            FROM mou_academia
        '''
        cursor.execute(query)
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Guest Speakers
@app.route('/get_guest_speakers', methods=['GET'])
def get_guest_speakers():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT gs.id, gs.name, gs.designation, gs.visit_date, gs.purpose, 
                   gs.industry, gs.location, gs.remarks,
                   GROUP_CONCAT(gsd.department SEPARATOR ', ') AS departments
            FROM guest_speakers gs
            LEFT JOIN guest_speaker_departments gsd ON gs.id = gsd.guest_speaker_id
        '''
        
        if department:
            query += " WHERE gsd.department = %s"
            query += " GROUP BY gs.id"
            cursor.execute(query, (department,))
        else:
            query += " GROUP BY gs.id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Industrial Visits
@app.route('/get_industrial_visits', methods=['GET'])
def get_industrial_visits():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT iv.visit_id, iv.industry_name, iv.start_date, iv.end_date, iv.location, 
                   iv.beneficiaries, iv.total_students, iv.remarks,
                   GROUP_CONCAT(ivd.department_name SEPARATOR ', ') AS departments
            FROM industrial_visits iv
            LEFT JOIN industrial_visit_departments ivd ON iv.visit_id = ivd.visit_id
        '''
        
        if department:
            query += " WHERE ivd.department_name = %s"
            query += " GROUP BY iv.visit_id"
            cursor.execute(query, (department,))
        else:
            query += " GROUP BY iv.visit_id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# HRD/FDP/SDP Events
@app.route('/get_hrd_fdp_sdp_events', methods=['GET'])
def get_hrd_fdp_sdp_events():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT e.id, e.event_title, e.event_type, e.start_date, e.start_time, 
                   e.end_date, e.end_time, e.convener_name, e.convener_phone, 
                   e.coordinator_name, e.coordinator_phone, e.resource_person, 
                   e.resource_person_designation, e.resource_person_cuo, e.topic, 
                   e.resource_person_details, e.beneficiaries, e.student_participants, 
                   e.remarks, e.brochure_path,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years
            FROM hrd_fdp_sdp_events e
            LEFT JOIN hrd_fdp_sdp_event_departments ed ON e.id = ed.event_id
            LEFT JOIN hrd_fdp_sdp_event_branches eb ON e.id = eb.event_id
            LEFT JOIN hrd_fdp_sdp_event_years ey ON e.id = ey.event_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("ed.department = %s")
            params.append(department)
        if year:
            conditions.append("ey.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY e.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Conferences
@app.route('/get_conferences', methods=['GET'])
def get_conferences():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT c.id, c.event_title, c.conference_url, c.start_date, c.start_time, 
                   c.end_date, c.end_time, c.convener_name, c.convener_phone, 
                   c.treasurer_name, c.treasurer_phone, c.papers_received, 
                   c.papers_accepted, c.indexing, c.quartile_ranking, 
                   c.contact_email, c.contact_phone, c.remarks, c.brochure_path,
                   GROUP_CONCAT(cd.department SEPARATOR ', ') AS departments
            FROM conferences c
            LEFT JOIN conference_departments cd ON c.id = cd.conference_id
        '''
        
        if department:
            query += " WHERE cd.department = %s"
            query += " GROUP BY c.id"
            cursor.execute(query, (department,))
        else:
            query += " GROUP BY c.id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Workshops/Seminars/Guest Lectures
@app.route('/get_workshops_seminars', methods=['GET'])
def get_workshops_seminars():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT w.id, w.event_name, w.national_international, w.event_type, 
                   w.start_date, w.end_date, w.topic, w.beneficiaries, 
                   w.student_participants, w.remarks,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years
            FROM workshops_seminars_guest_lectures w
            LEFT JOIN event_departments ed ON w.id = ed.event_id
            LEFT JOIN event_branches eb ON w.id = eb.event_id
            LEFT JOIN event_years ey ON w.id = ey.event_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("ed.department = %s")
            params.append(department)
        if year:
            conditions.append("ey.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY w.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Hackathons
@app.route('/get_hackathons', methods=['GET'])
def get_hackathons():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT h.id, h.hackathon_name, h.start_date, h.end_date, h.start_time, 
                   h.campus_allowed, h.team_limit, h.prize_details, h.winner_details, 
                   h.runner_details, h.second_runner_details, h.remarks, h.students_participated,
                   GROUP_CONCAT(DISTINCT hd.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT hy.year SEPARATOR ', ') AS years_allowed
            FROM hackathons h
            LEFT JOIN hackathon_departments hd ON h.id = hd.hackathon_id
            LEFT JOIN hackathon_years_allowed hy ON h.id = hy.hackathon_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("hd.department = %s")
            params.append(department)
        if year:
            conditions.append("hy.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY h.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# NSS Activities
@app.route('/get_nss_activities', methods=['GET'])
def get_nss_activities():
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT n.id, n.activity_name, n.start_date, n.end_date, n.start_time, 
                   n.purpose, n.coordinator_details, n.resource_person_details, 
                   n.remarks, n.students_participated,
                   GROUP_CONCAT(DISTINCT nya.year SEPARATOR ', ') AS years_allowed
            FROM nss_activities n
            LEFT JOIN nss_years_allowed nya ON n.id = nya.activity_id
        '''
        
        if year:
            query += " WHERE nya.year = %s"
            query += " GROUP BY n.id"
            cursor.execute(query, (year,))
        else:
            query += " GROUP BY n.id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# IIC/IEDC/MSME Activities
@app.route('/get_iic_iedc_msme_activities', methods=['GET'])
def get_iic_iedc_msme_activities():
    conducted_by = request.args.get('conducted_by', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT i.id, i.activity_name, i.start_date, i.end_date, i.students_participated, 
                   i.organizer_details, i.resource_person_details, i.significance, i.remarks,
                   GROUP_CONCAT(DISTINCT acb.conducted_by SEPARATOR ', ') AS conducted_by,
                   GROUP_CONCAT(DISTINCT aya.year SEPARATOR ', ') AS years_allowed
            FROM iic_iedc_msme_activities i
            LEFT JOIN activity_conducted_by acb ON i.id = acb.activity_id
            LEFT JOIN activity_years_allowed aya ON i.id = aya.activity_id
        '''
        
        conditions = []
        params = []
        
        if conducted_by:
            conditions.append("acb.conducted_by = %s")
            params.append(conducted_by)
        if year:
            conditions.append("aya.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY i.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Engineers Day Events
@app.route('/get_engineers_day_events', methods=['GET'])
def get_engineers_day_events():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT e.id, e.event_name, e.event_date, e.students_participated, 
                   e.details, e.brochure_path,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years_allowed
            FROM engineers_day_events e
            LEFT JOIN engineers_day_departments ed ON e.id = ed.event_id
            LEFT JOIN engineers_day_branches eb ON e.id = eb.event_id
            LEFT JOIN event_years_allowed ey ON e.id = ey.event_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("ed.department = %s")
            params.append(department)
        if year:
            conditions.append("ey.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY e.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# IB Tech Activities
@app.route('/get_ibtech_activities', methods=['GET'])
def get_ibtech_activities():
    department = request.args.get('department', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT i.id, i.activity_name, i.activity_type, i.start_date, i.end_date, 
                   i.coordinator_details, i.resource_person_details, 
                   i.students_participated, i.remarks,
                   GROUP_CONCAT(DISTINCT acd.department SEPARATOR ', ') AS conducted_departments
            FROM ibtech_activities i
            LEFT JOIN activity_conducted_departments acd ON i.id = acd.activity_id
        '''
        
        if department:
            query += " WHERE acd.department = %s"
            query += " GROUP BY i.id"
            cursor.execute(query, (department,))
        else:
            query += " GROUP BY i.id"
            cursor.execute(query)
            
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Parents Meetings
@app.route('/get_parents_meetings', methods=['GET'])
def get_parents_meetings():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT p.id, p.purpose, p.meeting_date, p.meeting_time, p.venue, 
                   p.coordinator_details, p.parents_attended, p.remarks,
                   GROUP_CONCAT(DISTINCT mcd.department SEPARATOR ', ') AS conducted_departments,
                   GROUP_CONCAT(DISTINCT my.year SEPARATOR ', ') AS years
            FROM parents_meetings p
            LEFT JOIN meeting_conducted_departments mcd ON p.id = mcd.meeting_id
            LEFT JOIN meeting_years my ON p.id = my.meeting_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("mcd.department = %s")
            params.append(department)
        if year:
            conditions.append("my.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY p.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# R&D Events
@app.route('/get_rd_events', methods=['GET'])
def get_rd_events():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT r.id, r.event_name, r.event_date, r.coordinator_details, 
                   r.resource_person_details, r.remarks, r.students_participated, r.brochure_path,
                   GROUP_CONCAT(DISTINCT red.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT rey.year SEPARATOR ', ') AS years_allowed
            FROM rd_events r
            LEFT JOIN rd_event_departments red ON r.id = red.event_id
            LEFT JOIN rd_event_years_allowed rey ON r.id = rey.event_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("red.department = %s")
            params.append(department)
        if year:
            conditions.append("rey.year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY r.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

# Fest Events
@app.route('/get_fest_events', methods=['GET'])
def get_fest_events():
    department = request.args.get('department', None)
    year = request.args.get('year', None)
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = '''
            SELECT f.id, f.fest_name, f.fest_date, f.fest_type, f.fest_significance, 
                   f.coordinator_details, f.resource_person_details, f.remarks, 
                   f.students_participated, f.brochure_path,
                   GROUP_CONCAT(DISTINCT fd.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT fsy.student_year SEPARATOR ', ') AS student_years
            FROM fest_events f
            LEFT JOIN fest_departments fd ON f.id = fd.fest_id
            LEFT JOIN fest_student_years fsy ON f.id = fsy.fest_id
        '''
        
        conditions = []
        params = []
        
        if department:
            conditions.append("fd.department = %s")
            params.append(department)
        if year:
            conditions.append("fsy.student_year = %s")
            params.append(year)
            
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
            
        query += " GROUP BY f.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

@app.route('/submit_laboratories', methods=['POST'])
def submit_lab_details():
    if request.method == 'POST':
        lab_name = request.form['labName']
        department = request.form['departmeNT']
        equipment_name = request.form['equipmentName']
        quantity = request.form['Equipmentquantity']
        cost = request.form['Equipmentcost']
        purchase_date = request.form['equipmentpurchaseddate']
        company_name = request.form['equipmentcompanyname']
        specifications = request.form['equipmentspecifications']
        remarks = request.form['Laboratoryremarks']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO laboratory_purchases (lab_name, department, equipment_name, quantity, cost, purchase_date, company_name, specifications, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (lab_name, department, equipment_name, quantity, cost, purchase_date, company_name, specifications, remarks))
            conn.commit()
            flash('Data inserted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('page4_dept'))

@app.route('/submit_student_chapters', methods=['POST'])
def submit_student_chapters():
    event_name = request.form.get("studentchaptersEventname")
    start_date = request.form.get("studentchapterStartingDate")
    end_date = request.form.get("studentchapterEndingDate")
    venue = request.form.get("studentchapterVenue")
    resource_person = request.form.get("studentchapterRSPname")
    college = request.form.get("studentchapterclg")
    participant_count = request.form.get("studentchapterparticipantcount")
    details = request.form.get("studentchapterdetails")
    departments = request.form.getlist("departmENt")  # Get all selected departments

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert event into student_chapters
        cursor.execute("""
            INSERT INTO student_chapters (event_name, start_date, end_date, venue, resource_person, college, participant_count, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (event_name, start_date, end_date, venue, resource_person, college, participant_count, details))
        conn.commit()

        event_id = cursor.lastrowid  # Get the last inserted event ID

        # Insert selected departments into student_chapter_departments
        for dept in departments:
            cursor.execute("""
                INSERT INTO student_chapter_departments (chapter_id, department)
                VALUES (%s, %s)
            """, (event_id, dept))
        
        conn.commit()
        flash('Event details inserted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_higher_education', methods=['POST'])
def submit_higher_education():
    if request.method == 'POST':
        student_name = request.form.get("highereducationstudentname")
        reg_number = request.form.get("highereducationstudentregnumber")
        department = request.form.get("departMEnt")
        exam_type = request.form.get("highereducationExamType")
        exam_rank = request.form.get("highereducationexamRank", 0)  # Default to 0 if empty
        exam_score = request.form.get("highereducationexamScore", 0)  # Default to 0 if empty
        course = request.form.get("highereducationCourse")
        admitted_college = request.form.get("highereducationAdmittedCollege")
        location = request.form.get("highereducationcollegeLocation")
        remarks = request.form.get("highereducationRemarks", "")

        # Debugging: Print received form data
        print(f"Received form data: {student_name}, {reg_number}, {department}, {exam_type}, {exam_rank}, {exam_score}, {course}, {admitted_college}, {location}, {remarks}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO higher_education 
                (student_name, register_number, department, exam_type, exam_rank, exam_score, course, admitted_college, location, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, reg_number, department, exam_type, exam_rank, exam_score, course, admitted_college, location, remarks))
            
            conn.commit()
            print('Higher education data inserted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            print(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4_dept'))
    
@app.route('/submit_internship', methods=['POST'])
def submit_internship():
    if request.method == 'POST':
        student_name = request.form.get("internshipStudentname")
        reg_number = request.form.get("internshipstudentRegisternumber")
        department = request.form.get("deparTMent")
        allowed_year = request.form.get("intershipallowedyear")
        company_name = request.form.get("internshipCompanyName")
        company_details = request.form.get("internshipCompanyDetails")
        start_date = request.form.get("internshipstdate")
        end_date = request.form.get("internshipeddate")
        duration = request.form.get("internshipDuration")
        designation = request.form.get("internshipdsgn")
        stipend = request.form.get("internshipStipend", 0)  # Default to 0 if empty
        mode = request.form.get("internshiponlineoffline")
        location = request.form.get("internshiplocation")
        remarks = request.form.get("internshipremarks", "")

        # Debugging: Print received form data
        print(f"Received form data: {student_name}, {reg_number}, {department}, {allowed_year}, {company_name}, {company_details}, {start_date}, {end_date}, {duration}, {designation}, {stipend}, {mode}, {location}, {remarks}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO internship_opportunities
                (student_name, register_number, department, allowed_year, company_name, company_details, start_date, end_date, duration, designation, stipend, mode, location, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (student_name, reg_number, department, allowed_year, company_name, company_details, start_date, end_date, duration, designation, stipend, mode, location, remarks))
            
            conn.commit()
            flash('Internship data inserted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4_dept'))
    
@app.route('/submit_alumni', methods=['POST'])
def submit_alumni():
    if request.method == 'POST':
        alumniname = request.form.get("Alumniname")
        talk_title = request.form.get("Alumnitalktitle")
        event_date = request.form.get("alumnieventdate")
        beneficiaries = request.form.get("alumniBeneficiaries")
        alumnijob = request.form.get("alumnijob")
        alumniregdno = request.form.get("alumniregdno")
        company_details = request.form.get("alumnicompdetails")
        department = request.form.get("aluminideparTMent")
        participants = request.form.get("aluminiparticipants", 0)  # Default to 0 if empty
        remarks = request.form.get("alumniremarks", "")

        # Debugging: Print received form data
        print(f"Received form data: {alumniname}, {talk_title}, {event_date}, {beneficiaries}, {alumnijob}, {alumniregdno}, {company_details}, {department}, {participants}, {remarks}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO alumni_cell
                (alumni_name, talk_title, event_date, beneficiaries, alumni_job, alumni_regdno, company_details, department, participants, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (alumniname, talk_title, event_date, beneficiaries, alumnijob, alumniregdno, company_details, department, participants, remarks))
            
            conn.commit()
            flash('Alumni event data inserted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4_dept'))
    
@app.route('/submit_mou', methods=['POST'])
def submit_mou():
    if request.method == 'POST':
        university = request.form.get("MOUuniversity")
        contact_person = request.form.get("MOUContactPerson")
        designation = request.form.get("MOUContactPersonDesignation")
        start_date = request.form.get("MOUstdate")
        end_date = request.form.get("MOUenddate")
        mou_period = request.form.get("MOUperiod")
        purpose = request.form.get("MOUpurpose")
        remarks = request.form.get("MOUremarks", "")

        # Handling File Upload
        file = request.files["MOUfileUpload"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Debugging: Print received form data
        print(f"Received: {university}, {contact_person}, {designation}, {start_date}, {end_date}, {mou_period}, {purpose}, {file_path}, {remarks}")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO mou_academia
                (university, contact_person, designation, start_date, end_date, mou_period, purpose, file_path, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (university, contact_person, designation, start_date, end_date, mou_period, purpose, file_path, remarks))
            
            conn.commit()
            flash('MOU data inserted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('page4_dept'))
    
@app.route('/submit_guest_speaker', methods=['POST'])
def submit_guest_speaker():
    name = request.form.get("speakerName")
    designation = request.form.get("speakerDesignation")
    visit_date = request.form.get("visitDate")
    purpose = request.form.get("visitPurpose")
    industry = request.form.get("speakerIndustry")
    location = request.form.get("speakerLocation")
    remarks = request.form.get("speakerRemarks")
    departments = request.form.getlist("departments")  # Get selected departments
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert into guest_speakers table
        cursor.execute("""
            INSERT INTO guest_speakers (name, designation, visit_date, purpose, industry, location, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, designation, visit_date, purpose, industry, location, remarks))
        conn.commit()
        speaker_id = cursor.lastrowid  # Get last inserted ID
        # Insert into guest_speaker_departments table
        for dept in departments:
            cursor.execute("INSERT INTO guest_speaker_departments (guest_speaker_id, department) VALUES (%s, %s)", (speaker_id, dept))
        conn.commit()
        flash('Guest speaker details inserted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('page4_dept'))

@app.route('/submit_industrial_visit', methods=['POST'])
def submit_industrial_visit():
    industry_name = request.form.get("organizedindustryname")
    start_date = request.form.get("organizedindustryVistedstDate")
    end_date = request.form.get("organizedindustryVistedendDate")
    location = request.form.get("organizedindustrylocation")
    beneficiaries = request.form.get("organisedindustryBeneficiaries")
    total_students = request.form.get("organisedindustrystudentparticipants")
    remarks = request.form.get("organisedindustryremarks")
    departments = request.form.getlist("industrialvisitdepaRTment")  # Get selected departments

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert into industrial_visits table
        cursor.execute("""
            INSERT INTO industrial_visits (industry_name, start_date, end_date, location, beneficiaries, total_students, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (industry_name, start_date, end_date, location, beneficiaries, total_students, remarks))
        conn.commit()

        visit_id = cursor.lastrowid  # Get last inserted ID

        # Insert into industrial_visit_departments table
        for dept in departments:
            cursor.execute("INSERT INTO industrial_visit_departments (visit_id, department_name) VALUES (%s, %s)", (visit_id, dept))

        conn.commit()
        flash('Industrial visit details inserted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error: {str(e)}', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('page4_dept'))  # Redirect to the main page or another route

@app.route('/submit_hrd_fdp_sdp', methods=['POST'])
def submit_hrd_fdp_sdp():
    if request.method == 'POST':
        # Extract form data
        event_title = request.form['conductedhrdname']
        event_type = request.form['conductedHRDFDPSDP']
        start_date = request.form['conductedhrdstartingdate']
        start_time = request.form['conductedhrdstartingtime']
        end_date = request.form['conductedhrdendingdate']
        end_time = request.form['conductedhrdendingtime']
        convener_name = request.form['conductedhrdConvener']
        convener_phone = request.form['conductedConvenerphnumber']
        coordinator_name = request.form['conductedhrdCoordinator']
        coordinator_phone = request.form['conductedhrdCoordinatorphnumber']
        resource_person = request.form['conductedhrdResoursePerson']
        resource_person_designation = request.form['conductedhrdResoursePersonDesignation']
        resource_person_cuo = request.form['conductedhrdresourcepersonCUO']
        topic = request.form['conductedhrdtopic']
        resource_person_details = request.form['resourcepersondetails']
        beneficiaries = request.form['conductedhrdbeneficiaries']
        student_participants = request.form['conductedhrdstudentparticipants']
        remarks = request.form['conductedhrdremarks']
        file = request.files["conductedhrdBrochureUpload"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        # Handle file upload
        # Get multiple values from checkboxes
        departments = request.form.getlist('depaRTment')
        branches = request.form.getlist('conductedhrdbranch')
        years = request.form.getlist('conductedhrdyear')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main events table
            cursor.execute('''
                INSERT INTO hrd_fdp_sdp_events
                (event_title, event_type, start_date, start_time, end_date, end_time, convener_name, convener_phone, coordinator_name, coordinator_phone, resource_person, resource_person_designation, resource_person_cuo, topic, resource_person_details, beneficiaries, student_participants, remarks, brochure_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (event_title, event_type, start_date, start_time, end_date, end_time, convener_name, convener_phone, coordinator_name, coordinator_phone, resource_person, resource_person_designation, resource_person_cuo, topic, resource_person_details, beneficiaries, student_participants, remarks, file_path))
            conn.commit()

            # Get the last inserted event ID
            event_id = cursor.lastrowid

            # Insert departments into event_departments table
            for dept in departments:
                cursor.execute("INSERT INTO hrd_fdp_sdp_event_departments (event_id, department) VALUES (%s, %s)", (event_id, dept))

            # Insert branches into event_branches table
            for branch in branches:
                cursor.execute("INSERT INTO hrd_fdp_sdp_event_branches (event_id, branch) VALUES (%s, %s)", (event_id, branch))

            # Insert years into event_years table
            for year in years:
                cursor.execute("INSERT INTO hrd_fdp_sdp_event_years (event_id, year) VALUES (%s, %s)", (event_id, year))


            conn.commit()
            flash('HRD/FDP/SDP event submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('page4_dept'))
    
@app.route('/submit_conference', methods=['POST'])
def submit_conference():
    if request.method == 'POST':
        # Extract form data
        event_title = request.form['conductedconferencename']
        conference_url = request.form['cnductedConferenceURL']
        start_date = request.form['conductedconferenceSTDate']
        start_time = request.form['conductedconferenceSTTime']
        end_date = request.form['conductedconferenceENDate']
        end_time = request.form['conductedconferenceENTime']
        convener_name = request.form['conductedconferenceConvener']
        convener_phone = request.form['conductedconferenceConvenerphnumber']
        treasurer_name = request.form['conductedconferenceTreasurer']
        treasurer_phone = request.form['conductedconferenceTreasurerphnumber']
        papers_received = request.form['conductedconferencePapersreceived']
        papers_accepted = request.form['conductedconferencePapersaccepted']
        indexing = request.form['conductedconferenceIndexing']
        quartile_ranking = request.form['conductedconferenceQuartileRanking']
        contact_email = request.form['conductedconferenceContactEmail']
        contact_phone = request.form['conductedconferenceContactPhoneNumber']
        remarks = request.form['conductedconferenceremarks']
        file = request.files["conductedconferenceUploadBrochure"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Get multiple values from checkboxes (departments)
        departments = request.form.getlist('depARtment')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main conferences table
            cursor.execute('''
                INSERT INTO conferences
                (event_title, conference_url, start_date, start_time, end_date, end_time, convener_name, convener_phone, treasurer_name, treasurer_phone, papers_received, papers_accepted, indexing, quartile_ranking, contact_email, contact_phone, remarks, brochure_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (event_title, conference_url, start_date, start_time, end_date, end_time, convener_name, convener_phone, treasurer_name, treasurer_phone, papers_received, papers_accepted, indexing, quartile_ranking, contact_email, contact_phone, remarks, file_path))
            conn.commit()

            # Get the last inserted conference ID
            conference_id = cursor.lastrowid

            # Insert departments into conference_departments table
            for dept in departments:
                cursor.execute("INSERT INTO conference_departments (conference_id, department) VALUES (%s, %s)", (conference_id, dept))

            conn.commit()
            flash('Conference details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))

@app.route('/submit_workshop_seminar_guest_lecture', methods=['POST'])
def submit_workshop_seminar_guest_lecture():
    if request.method == 'POST':
        # Extract form data
        event_name = request.form['conductedworkshopname']
        national_international = request.form['conductedworkshopNI']
        event_type = request.form['conductedwgs']
        start_date = request.form['conductedworkshopstDate']
        end_date = request.form['conductedworkshopendDate']
        topic = request.form['conductedworkshoptopic']
        beneficiaries = request.form['conductedworkshopbeneficiaries']
        student_participants = request.form['conductedworkshopstudentparticipants']
        remarks = request.form['conductedwsremarks']

        # Get multiple values from checkboxes
        departments = request.form.getlist('dePArtment')
        branches = request.form.getlist('conductedwsbranch')
        years = request.form.getlist('conductedwsstudentsyear')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main workshops_seminars_guest_lectures table
            cursor.execute('''
                INSERT INTO workshops_seminars_guest_lectures
                (event_name, national_international, event_type, start_date, end_date, topic, beneficiaries, student_participants, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (event_name, national_international, event_type, start_date, end_date, topic, beneficiaries, student_participants, remarks))
            conn.commit()

            # Get the last inserted event ID
            event_id = cursor.lastrowid

            # Insert departments into event_departments table
            for dept in departments:
                cursor.execute("INSERT INTO event_departments (event_id, department) VALUES (%s, %s)", (event_id, dept))

            # Insert branches into event_branches table
            for branch in branches:
                cursor.execute("INSERT INTO event_branches (event_id, branch) VALUES (%s, %s)", (event_id, branch))

            # Insert years into event_years table
            for year in years:
                cursor.execute("INSERT INTO event_years (event_id, year) VALUES (%s, %s)", (event_id, year))

            conn.commit()
            flash('Workshop/Seminar/Guest Lecture details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_hackathon', methods=['POST'])
def submit_hackathon():
    if request.method == 'POST':
        # Extract form data
        hackathon_name = request.form['hackthonconductedName']
        start_date = request.form['conductedhackthondate']
        end_date = request.form['conductedHackthonenddate']
        start_time = request.form['conductedhackthonStartingTime']
        campus_allowed = request.form['conductedhackthonCampusallowed']
        team_limit = request.form['conductedhackthonTeamLimit']
        prize_details = request.form['conductedhackthonpriceDetails']
        winner_details = request.form['conductedhackthonWinnerDetails']
        runner_details = request.form['conductedhackthonRunnerDetails']
        second_runner_details = request.form['conductedhackthonSecondRunnerDetails']
        remarks = request.form['conductedHackthonRemarks']
        students_participated = request.form['conductedhackthonStudentsParticipation']

        # Get multiple values from checkboxes
        departments = request.form.getlist('dEPartment')
        years_allowed = request.form.getlist('conductedhackthonStudentsAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main hackathons table
            cursor.execute('''
                INSERT INTO hackathons 
                (hackathon_name, start_date, end_date, start_time, campus_allowed, team_limit, prize_details, winner_details, runner_details, second_runner_details, remarks, students_participated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (hackathon_name, start_date, end_date, start_time, campus_allowed, team_limit, prize_details, winner_details, runner_details, second_runner_details, remarks, students_participated))
            conn.commit()

            # Get the last inserted hackathon ID
            hackathon_id = cursor.lastrowid

            # Insert departments into hackathon_departments table
            for dept in departments:
                cursor.execute("INSERT INTO hackathon_departments (hackathon_id, department) VALUES (%s, %s)", (hackathon_id, dept))

            # Insert years allowed into hackathon_years_allowed table
            for year in years_allowed:
                cursor.execute("INSERT INTO hackathon_years_allowed (hackathon_id, year) VALUES (%s, %s)", (hackathon_id, year))

            conn.commit()
            flash('Hackathon details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_nss_activity', methods=['POST'])
def submit_nss_activity():
    if request.method == 'POST':
        # Extract form data
        activity_name = request.form['nssactivityname']
        start_date = request.form['nssactivitystdate']
        end_date = request.form['nssactivityenddate']
        start_time = request.form['nssactivitysttime']
        purpose = request.form['nssactivitypurpose']
        coordinator_details = request.form['nsscoordinatordetails']
        resource_person_details = request.form['nssresourcepersondetails']
        remarks = request.form['nssactivityRemarks']
        students_participated = request.form['nssStudentsParticipation']

        # Get multiple values from checkboxes (years allowed)
        years_allowed = request.form.getlist('nssStudentsAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main nss_activities table
            cursor.execute('''
                INSERT INTO nss_activities 
                (activity_name, start_date, end_date, start_time, purpose, coordinator_details, resource_person_details, remarks, students_participated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (activity_name, start_date, end_date, start_time, purpose, coordinator_details, resource_person_details, remarks, students_participated))
            conn.commit()

            # Get the last inserted activity ID
            activity_id = cursor.lastrowid

            # Insert years allowed into nss_years_allowed table
            for year in years_allowed:
                cursor.execute("INSERT INTO nss_years_allowed (activity_id, year) VALUES (%s, %s)", (activity_id, year))

            conn.commit()
            flash('NSS activity details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_iic_iedc_msme_activity', methods=['POST'])
def submit_iic_iedc_msme_activity():
    if request.method == 'POST':
        # Extract form data
        activity_name = request.form['iiceventName']
        start_date = request.form['iicactivitystartingdate']
        end_date = request.form['iicactivityEndingdate']
        students_participated = request.form['iicactivitystudentsparticipants']
        organizer_details = request.form['iicactivitypriceDetails']
        resource_person_details = request.form['iicactivityWinnerDetails']
        significance = request.form['iicactivityRunnerDetails']
        remarks = request.form['iicactivityremarks']

        # Get multiple values from checkboxes
        conducted_by = request.form.getlist('iicConducted')
        years_allowed = request.form.getlist('iicStudentsAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main iic_iedc_msme_activities table
            cursor.execute('''
                INSERT INTO iic_iedc_msme_activities 
                (activity_name, start_date, end_date, students_participated, organizer_details, resource_person_details, significance, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (activity_name, start_date, end_date, students_participated, organizer_details, resource_person_details, significance, remarks))
            conn.commit()

            # Get the last inserted activity ID
            activity_id = cursor.lastrowid

            # Insert conducted_by into activity_conducted_by table
            for conducted in conducted_by:
                cursor.execute("INSERT INTO activity_conducted_by (activity_id, conducted_by) VALUES (%s, %s)", (activity_id, conducted))

            # Insert years allowed into activity_years_allowed table
            for year in years_allowed:
                cursor.execute("INSERT INTO activity_years_allowed (activity_id, year) VALUES (%s, %s)", (activity_id, year))

            conn.commit()
            flash('IIC/IEDC/ECELL/MSME activity details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_engineers_day', methods=['POST'])
def submit_engineers_day():
    if request.method == 'POST':
        # Extract form data
        event_name = request.form['engineersdayname']
        event_date = request.form['EngineersdayDate']
        students_participated = request.form['engineersdaystudparticipant']
        details = request.form['engineersdaydetails']
        file = request.files["engineersdayUploadBrochure"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Get multiple values from checkboxes
        departments = request.form.getlist('DEpartment')
        branches = request.form.getlist('engineersdaybranch')
        years_allowed = request.form.getlist('engineersdayAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main engineers_day_events table
            cursor.execute('''
                INSERT INTO engineers_day_events
                (event_name, event_date, students_participated, details, brochure_path)
                VALUES (%s, %s, %s, %s, %s)
            ''', (event_name, event_date, students_participated, details, file_path))
            conn.commit()

            # Get the last inserted event ID
            event_id = cursor.lastrowid

            # Insert departments into event_departments table
            for dept in departments:
                cursor.execute("INSERT INTO engineers_day_departments (event_id, department) VALUES (%s, %s)", (event_id, dept))

            # Insert branches into event_branches table
            for branch in branches:
                cursor.execute("INSERT INTO engineers_day_branches (event_id, branch) VALUES (%s, %s)", (event_id, branch))

            # Insert years allowed into event_years_allowed table
            for year in years_allowed:
                cursor.execute("INSERT INTO event_years_allowed (event_id, year) VALUES (%s, %s)", (event_id, year))

            conn.commit()
            flash('Engineers Day event details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_ibtech_activity', methods=['POST'])
def submit_ibtech_activity():
    if request.method == 'POST':
        # Extract form data
        activity_name = request.form['istbtechactivityName']
        activity_type = request.form['istbtechactivitytype']
        start_date = request.form['istbtechdate']
        end_date = request.form['istbtechendingdate']
        coordinator_details = request.form['istbtechcoordinatorDetails']
        resource_person_details = request.form['istbtechresourcepersondetails']
        students_participated = request.form['istbtechStudentsParticipation']
        remarks = request.form['istbtechStudentsremarks']

        # Get multiple values from checkboxes
        conducted_departments = request.form.getlist('istbtechactivityconducteddept')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main ibtech_activities table
            cursor.execute('''
                INSERT INTO ibtech_activities 
                (activity_name, activity_type, start_date, end_date, coordinator_details, resource_person_details, students_participated, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (activity_name, activity_type, start_date, end_date, coordinator_details, resource_person_details, students_participated, remarks))
            conn.commit()

            # Get the last inserted activity ID
            activity_id = cursor.lastrowid

            # Insert conducted departments into activity_conducted_departments table
            for dept in conducted_departments:
                cursor.execute("INSERT INTO activity_conducted_departments (activity_id, department) VALUES (%s, %s)", (activity_id, dept))

            conn.commit()
            flash('I B.Tech activity details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_parents_meeting', methods=['POST'])
def submit_parents_meeting():
    if request.method == 'POST':
        # Extract form data
        purpose = request.form['meetingpurpose']
        meeting_date = request.form['meetingdate']
        meeting_time = request.form['meetingtime']
        venue = request.form['Venueofmeeting']
        coordinator_details = request.form['pmcoordinatordetails']
        parents_attended = request.form['Numberofparentsattended']
        remarks = request.form['meetingremarks']

        # Get multiple values from checkboxes
        conducted_departments = request.form.getlist('meetingconducteddept')
        years = request.form.getlist('parentsyear')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main parents_meetings table
            cursor.execute('''
                INSERT INTO parents_meetings 
                (purpose, meeting_date, meeting_time, venue, coordinator_details, parents_attended, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (purpose, meeting_date, meeting_time, venue, coordinator_details, parents_attended, remarks))
            conn.commit()

            # Get the last inserted meeting ID
            meeting_id = cursor.lastrowid

            # Insert conducted departments into meeting_conducted_departments table
            for dept in conducted_departments:
                cursor.execute("INSERT INTO meeting_conducted_departments (meeting_id, department) VALUES (%s, %s)", (meeting_id, dept))

            # Insert years into meeting_years table
            for year in years:
                cursor.execute("INSERT INTO meeting_years (meeting_id, year) VALUES (%s, %s)", (meeting_id, year))

            conn.commit()
            flash('Parents meeting details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_rd_event', methods=['POST'])
def submit_rd_event():
    if request.method == 'POST':
        # Extract form data
        event_name = request.form['radname']
        event_date = request.form['radactivitydate']
        coordinator_details = request.form['radcoordinatordetails']
        resource_person_details = request.form['radresourcepersondetails']
        remarks = request.form['radactivityRemarks']
        students_participated = request.form['radStudentsParticipation']
        file = request.files["radUploadBrochure"]
        file_path = ""
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Get multiple values from checkboxes
        departments = request.form.getlist('radconducteddept')
        years_allowed = request.form.getlist('radStudentsAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main rd_events table
            cursor.execute('''
                INSERT INTO rd_events
                (event_name, event_date, coordinator_details, resource_person_details, remarks, students_participated, brochure_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (event_name, event_date, coordinator_details, resource_person_details, remarks, students_participated, file_path))
            conn.commit()

            # Get the last inserted event ID
            event_id = cursor.lastrowid

            # Insert departments into event_departments table
            for dept in departments:
                cursor.execute("INSERT INTO rd_event_departments (event_id, department) VALUES (%s, %s)", (event_id, dept))

            # Insert years allowed into event_years_allowed table
            for year in years_allowed:
                cursor.execute("INSERT INTO rd_event_years_allowed (event_id, year) VALUES (%s, %s)", (event_id, year))

            conn.commit()
            flash('R&D Event details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/submit_fest', methods=['POST'])
def submit_fest():
    if request.method == 'POST':
        # Extract form data
        fest_name = request.form['festname']
        fest_date = request.form['festdate']
        fest_type = request.form['festtype']
        fest_significance = request.form['festsignificance']
        fest_coordinator_details = request.form['festcoordinatordetails']
        fest_resource_person_details = request.form['festresourcepersondetails']
        fest_remarks = request.form['festRemarks']
        fest_students_participated = request.form['radStudentsParticipation']
        
        # Handle file upload
        file_path = ""
        if 'festUploadBrochure' in request.files:
            file = request.files['festUploadBrochure']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

        # Get multiple values from checkboxes
        departments = request.form.getlist('festconducteddept')
        student_years = request.form.getlist('festStudentsAllowed')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert into main fest_events table
            cursor.execute('''
                INSERT INTO fest_events 
                (fest_name, fest_date, fest_type, fest_significance, coordinator_details, 
                resource_person_details, remarks, students_participated, brochure_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (fest_name, fest_date, fest_type, fest_significance, fest_coordinator_details, fest_resource_person_details, fest_remarks, fest_students_participated, file_path))
            conn.commit()

            # Get the last inserted event ID
            fest_id = cursor.lastrowid

            # Insert departments into fest_departments table
            for dept in departments:
                cursor.execute("INSERT INTO fest_departments (fest_id, department) VALUES (%s, %s)", (fest_id, dept))

            # Insert student years into fest_student_years table
            for year in student_years:
                cursor.execute("INSERT INTO fest_student_years (fest_id, student_year) VALUES (%s, %s)", (fest_id, year))

            conn.commit()
            flash('Fest details submitted successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('page4_dept'))
    
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/hods/add_user', methods=['GET', 'POST'])
def add_user_hods():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        table_map = {
            'faculty': 'faculty',
            'dept': 'dept',
            'studentclubs': 'studentclubs',
            'startups': 'startups',
            'login1': 'login1',
            'hods': 'hods',
        }
        table = table_map.get(user_type)
        if not table:
            flash('Invalid user type selected.', 'danger')
            return redirect(url_for('add_user_hods'))

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if user_type == 'faculty':
                faculty_name = request.form.get('faculty_name')
                department = request.form.get('department')
                if not faculty_name or not department:
                    flash('Faculty Name and Department are required for faculty users.', 'danger')
                    return redirect(url_for('add_user_hods'))
                # Insert into faculty first
                cursor.execute("INSERT INTO faculty (user_id, password) VALUES (%s, %s)", (user_id, password))
                # Then insert into faculty_details
                cursor.execute("INSERT INTO faculty_details (user_id, faculty_name, department) VALUES (%s, %s, %s)", (user_id, faculty_name, department))
            else:
                # For other user types
                cursor.execute(f"INSERT INTO {table} (user_id, password) VALUES (%s, %s)", (user_id, password))

            conn.commit()
            flash('User added successfully!', 'success')
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            if e.errno == 1062:
                flash(f'Error: User ID "{user_id}" already exists.', 'danger')
            else:
                flash(f'Error adding user: {str(e)}', 'danger')
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'An unexpected error occurred: {str(e)}', 'danger')
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('add_user_hods'))
    return render_template('add_user.html')

@app.route('/hods/remove_user', methods=['GET', 'POST'])
def remove_user_hods():
    removed_users = []
    user_type_view = request.args.get('user_type_view')
    year_view = request.args.get('year_view')
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        user_id = request.form.get('user_id')
        relieving_date = request.form.get('relieving_date')
        table_map = {
            'faculty': 'faculty',
            'dept': 'dept',
            'studentclubs': 'studentclubs',
            'startups': 'startups',
            'login1': 'login1',
            'hods': 'hods',
        }
        table = table_map.get(user_type)
        if not table:
            flash('Invalid user type selected.', 'danger')
            return redirect(url_for('remove_user_hods'))
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # Create removed_users table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS removed_users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_type VARCHAR(50),
                    user_id VARCHAR(255),
                    password VARCHAR(255),
                    removed_at DATETIME,
                    extra_details JSON
                )
            ''')
            # Fetch user data
            cursor.execute(f"SELECT * FROM {table} WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            if not user_data:
                flash('User not found.', 'danger')
            else:
                extra_details = user_data.copy()
                password = extra_details.pop('password', None)
                extra_details.pop('user_id', None)
                # If faculty, also fetch faculty_details and add relieving_date
                if user_type == 'faculty':
                    cursor.execute("SELECT * FROM faculty_details WHERE user_id = %s", (user_id,))
                    faculty_details = cursor.fetchone()
                    if faculty_details:
                        extra_details['faculty_details'] = faculty_details
                    if relieving_date:
                        extra_details['relieving_date'] = relieving_date
                import json, datetime
                cursor.execute(
                    "INSERT INTO removed_users (user_type, user_id, password, removed_at, extra_details) VALUES (%s, %s, %s, %s, %s)",
                    (user_type, user_id, password, datetime.datetime.now(), json.dumps(extra_details))
                )
                # Explicitly delete from faculty_details before deleting from faculty
                if user_type == 'faculty':
                    cursor.execute("DELETE FROM faculty_details WHERE user_id = %s", (user_id,))
                cursor.execute(f"DELETE FROM {table} WHERE user_id = %s", (user_id,))
                conn.commit()
                flash('User removed successfully!', 'success')
            cursor.execute("SELECT * FROM removed_users ORDER BY removed_at DESC")
            removed_users = cursor.fetchall()
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f'Error removing user: {str(e)}', 'danger')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
        return render_template('remove_user.html', removed_users=removed_users, user_type_view=user_type_view, year_view=year_view)
    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            if user_type_view and year_view:
                cursor.execute("SELECT * FROM removed_users WHERE user_type = %s AND YEAR(removed_at) = %s ORDER BY removed_at DESC", (user_type_view, year_view))
                removed_users = cursor.fetchall()
            elif user_type_view:
                cursor.execute("SELECT * FROM removed_users WHERE user_type = %s ORDER BY removed_at DESC", (user_type_view,))
                removed_users = cursor.fetchall()
            else:
                removed_users = []
        except Exception:
            removed_users = []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
        return render_template('remove_user.html', removed_users=removed_users, user_type_view=user_type_view, year_view=year_view)

@app.route('/get_departments', methods=['GET'])
def get_departments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT department FROM faculty_details ORDER BY department')
        departments = [row[0] for row in cursor.fetchall()]
        return jsonify(departments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/get_faculty_names', methods=['GET'])
def get_faculty_names():
    department = request.args.get('department')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT faculty_name FROM faculty_details WHERE department = %s ORDER BY faculty_name', (department,))
        faculty_names = cursor.fetchall()
        return jsonify(faculty_names)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# Student Profile API Endpoints
@app.route('/get_student_names', methods=['GET'])
def get_student_names():
    department = request.args.get('department')
    if not department:
        return jsonify({'error': 'Department is required'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT DISTINCT student_name FROM publications WHERE department = %s ORDER BY student_name', (department,))
        student_names = cursor.fetchall()
        return jsonify(student_names)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/get_student_patents', methods=['GET'])
def get_student_patents():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT applicant_name, inventors, department, patent_title, patent_number, 
                   status, filed_date, published_date, granted_date
            FROM patents
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND (YEAR(filed_date) = %s OR YEAR(published_date) = %s OR YEAR(granted_date) = %s)'
            params.extend([year, year, year])
        if month:
            query += ' AND (MONTH(filed_date) = %s OR MONTH(published_date) = %s OR MONTH(granted_date) = %s)'
            params.extend([month, month, month])
        cursor.execute(query, tuple(params))
        patents = cursor.fetchall()
        return jsonify(patents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_journals', methods=['GET'])
def get_student_journals():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, journal_type, authors, journal_name, paper_title, issn, quartile_ranking, doi, volume, page, month_year
            FROM publications
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(month_year) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(month_year) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        journals = cursor.fetchall()
        return jsonify(journals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_conferences', methods=['GET'])
def get_student_conferences():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, scsswsg, authors_designation, conference_name, paper_title, issn, doi, volume, page, month_year
            FROM conference_publications
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(month_year) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(month_year) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        conferences = cursor.fetchall()
        return jsonify(conferences)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_workshops', methods=['GET'])
def get_student_workshops():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, event_name, national_international, event_type, event_date, organized_by
            FROM workshop_attendance
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(event_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(event_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        workshops = cursor.fetchall()
        return jsonify(workshops)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_achievements', methods=['GET'])
def get_student_achievements():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, achievement_name, awarded_by, achievement_date
            FROM student_achievements
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(achievement_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(achievement_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        achievements = cursor.fetchall()
        return jsonify(achievements)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_industry_visits', methods=['GET'])
def get_student_industry_visits():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, industry_name, visit_date, significance, location
            FROM industry_visits
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(visit_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(visit_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        visits = cursor.fetchall()
        return jsonify(visits)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_vedic_workshops', methods=['GET'])
def get_student_vedic_workshops():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, workshop_name, event_date, venue
            FROM vedic_workshops
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(event_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(event_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        workshops = cursor.fetchall()
        return jsonify(workshops)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_competitions', methods=['GET'])
def get_student_competitions():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, competition_name, organized_by, duration, level
            FROM outside_competitions
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(competition_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(competition_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        competitions = cursor.fetchall()
        return jsonify(competitions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_sports', methods=['GET'])
def get_student_sports():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, year, game_name, game_details, organized_by, venue, event_start_date, event_end_date, secured_position, level
            FROM sports_participation
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND year = %s'
            params.append(year)
        cursor.execute(query, tuple(params))
        sports = cursor.fetchall()
        return jsonify(sports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_certifications', methods=['GET'])
def get_student_certifications():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, course_title, duration, course_topic, details, certificate_path
            FROM certifications
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(certification_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(certification_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        certifications = cursor.fetchall()
        return jsonify(certifications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_student_nptel_courses', methods=['GET'])
def get_student_nptel_courses():
    department = request.args.get('department')
    student = request.args.get('student')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, department, course_title, duration, course_id, score, platform, details, certificate_path
            FROM nptel_courses
            WHERE department = %s
        '''
        params = [department]
        if student:
            query += ' AND student_name = %s'
            params.append(student)
        if year:
            query += ' AND YEAR(completion_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(completion_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        courses = cursor.fetchall()
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Department Profile API Endpoints
@app.route('/get_department_stats', methods=['GET'])
def get_department_stats():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get faculty count
        cursor.execute('SELECT COUNT(DISTINCT faculty_name) as total_faculty FROM faculty_details WHERE department = %s', (department,))
        faculty_count = cursor.fetchone()['total_faculty']
        
        # Get student count
        cursor.execute('SELECT COUNT(DISTINCT student_name) as total_students FROM publications WHERE department = %s', (department,))
        student_count = cursor.fetchone()['total_students']
        
        # Get patents count
        cursor.execute('SELECT COUNT(*) as total_patents FROM faculty_patents WHERE department = %s', (department,))
        patents_count = cursor.fetchone()['total_patents']
        
        # Get publications count
        cursor.execute('SELECT COUNT(*) as total_publications FROM faculty_journals WHERE department = %s', (department,))
        faculty_pubs = cursor.fetchone()['total_publications']
        cursor.execute('SELECT COUNT(*) as total_publications FROM faculty_conferences WHERE department = %s', (department,))
        faculty_conf = cursor.fetchone()['total_publications']
        cursor.execute('SELECT COUNT(*) as total_publications FROM publications WHERE department = %s', (department,))
        student_pubs = cursor.fetchone()['total_publications']
        cursor.execute('SELECT COUNT(*) as total_publications FROM conference_publications WHERE department = %s', (department,))
        student_conf = cursor.fetchone()['total_publications']
        total_publications = faculty_pubs + faculty_conf + student_pubs + student_conf
        
        # Get projects count
        cursor.execute('SELECT COUNT(*) as total_projects FROM research_grants WHERE department = %s', (department,))
        projects_count = cursor.fetchone()['total_projects']
        
        # Get achievements count
        cursor.execute('SELECT COUNT(*) as total_achievements FROM faculty_achievements WHERE department = %s', (department,))
        faculty_ach = cursor.fetchone()['total_achievements']
        cursor.execute('SELECT COUNT(*) as total_achievements FROM student_achievements WHERE department = %s', (department,))
        student_ach = cursor.fetchone()['total_achievements']
        total_achievements = faculty_ach + student_ach
        
        stats = {
            'total_faculty': faculty_count,
            'total_students': student_count,
            'total_patents': patents_count,
            'total_publications': total_publications,
            'total_projects': projects_count,
            'total_achievements': total_achievements
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_faculty_overview', methods=['GET'])
def get_department_faculty_overview():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT 
                fd.faculty_name,
                fd.designation,
                COALESCE(p.patents_count, 0) as patents_count,
                COALESCE(pub.publications_count, 0) as publications_count,
                COALESCE(proj.projects_count, 0) as projects_count,
                COALESCE(ach.achievements_count, 0) as achievements_count,
                COALESCE(cert.certifications_count, 0) as certifications_count
            FROM faculty_details fd
            LEFT JOIN (
                SELECT faculty_name, COUNT(*) as patents_count 
                FROM faculty_patents 
                WHERE department = %s GROUP BY faculty_name
            ) p ON fd.faculty_name = p.faculty_name
            LEFT JOIN (
                SELECT faculty_name, COUNT(*) as publications_count 
                FROM faculty_journals 
                WHERE department = %s GROUP BY faculty_name
            ) pub ON fd.faculty_name = pub.faculty_name
            LEFT JOIN (
                SELECT faculty_name, COUNT(*) as projects_count 
                FROM research_grants 
                WHERE department = %s GROUP BY faculty_name
            ) proj ON fd.faculty_name = proj.faculty_name
            LEFT JOIN (
                SELECT faculty_name, COUNT(*) as achievements_count 
                FROM faculty_achievements 
                WHERE department = %s GROUP BY faculty_name
            ) ach ON fd.faculty_name = ach.faculty_name
            LEFT JOIN (
                SELECT faculty_name, COUNT(*) as certifications_count 
                FROM faculty_certifications 
                WHERE department = %s GROUP BY faculty_name
            ) cert ON fd.faculty_name = cert.faculty_name
            WHERE fd.department = %s
        '''
        cursor.execute(query, (department, department, department, department, department, department))
        overview = cursor.fetchall()
        return jsonify(overview)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_faculty_patents', methods=['GET'])
def get_department_faculty_patents():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT faculty_id, faculty_name, patent_title, patent_number, status, filed_date, published_date, granted_date
            FROM faculty_patents
            WHERE department = %s
        '''
        params = [department]
        if year:
            query += ' AND (YEAR(filed_date) = %s OR YEAR(published_date) = %s OR YEAR(granted_date) = %s)'
            params.extend([year, year, year])
        if month:
            query += ' AND (MONTH(filed_date) = %s OR MONTH(published_date) = %s OR MONTH(granted_date) = %s)'
            params.extend([month, month, month])
        cursor.execute(query, tuple(params))
        patents = cursor.fetchall()
        return jsonify(patents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_faculty_publications', methods=['GET'])
def get_department_faculty_publications():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Combine journal and conference publications
        query = '''
            SELECT faculty_name, 'Journal' as publication_type, paper_title as title, journal_name as journal_conference, issn, doi, month_and_year
            FROM faculty_journals
            WHERE department = %s
            UNION ALL
            SELECT faculty_name, 'Conference' as publication_type, paper_title as title, conference_name as journal_conference, issn, doi, month_and_year
            FROM faculty_conferences
            WHERE department = %s
        '''
        params = [department, department]
        if year:
            query += ' AND YEAR(month_and_year) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(month_and_year) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        publications = cursor.fetchall()
        return jsonify(publications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_research_projects', methods=['GET'])
def get_department_research_projects():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT faculty_name, project_id, project_title, funding_agency, principle_investigator, co_pi, project_duration, total_grant_sanctioned
            FROM research_grants
            WHERE department = %s
        '''
        params = [department]
        if year:
            query += ' AND YEAR(project_duration) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(project_duration) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        projects = cursor.fetchall()
        return jsonify(projects)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_student_overview', methods=['GET'])
def get_department_student_overview():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT 
                p.student_name,
                p.registration_number,
                COALESCE(pub.publications_count, 0) as publications_count,
                COALESCE(pat.patents_count, 0) as patents_count,
                COALESCE(ach.achievements_count, 0) as achievements_count,
                COALESCE(cert.certifications_count, 0) as certifications_count,
                COALESCE(comp.competitions_count, 0) as competitions_count
            FROM publications p
            LEFT JOIN (
                SELECT student_name, COUNT(*) as publications_count 
                FROM publications 
                WHERE department = %s GROUP BY student_name
            ) pub ON p.student_name = pub.student_name
            LEFT JOIN (
                SELECT student_name, COUNT(*) as patents_count 
                FROM student_patents 
                WHERE department = %s GROUP BY student_name
            ) pat ON p.student_name = pat.student_name
            LEFT JOIN (
                SELECT student_name, COUNT(*) as achievements_count 
                FROM student_achievements 
                WHERE department = %s GROUP BY student_name
            ) ach ON p.student_name = ach.student_name
            LEFT JOIN (
                SELECT student_name, COUNT(*) as certifications_count 
                FROM certifications 
                WHERE department = %s GROUP BY student_name
            ) cert ON p.student_name = cert.student_name
            LEFT JOIN (
                SELECT student_name, COUNT(*) as competitions_count 
                FROM competitions 
                WHERE department = %s GROUP BY student_name
            ) comp ON p.student_name = comp.student_name
            WHERE p.department = %s
            GROUP BY p.student_name, p.registration_number
        '''
        cursor.execute(query, (department, department, department, department, department, department))
        overview = cursor.fetchall()
        return jsonify(overview)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_student_publications', methods=['GET'])
def get_department_student_publications():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Combine journal and conference publications
        query = '''
            SELECT student_name, registration_number, 'Journal' as publication_type, paper_title as title, journal_name as journal_conference, issn, doi, month_year
            FROM publications
            WHERE department = %s
            UNION ALL
            SELECT student_name, registration_number, 'Conference' as publication_type, paper_title as title, conference_name as journal_conference, issn, doi, month_year
            FROM conference_publications
            WHERE department = %s
        '''
        params = [department, department]
        if year:
            query += ' AND YEAR(month_year) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(month_year) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        publications = cursor.fetchall()
        return jsonify(publications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_student_achievements', methods=['GET'])
def get_department_student_achievements():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT student_name, registration_number, achievement_name, awarded_by, achievement_date, 'Academic' as category
            FROM student_achievements
            WHERE department = %s
        '''
        params = [department]
        if year:
            query += ' AND YEAR(achievement_date) = %s'
            params.append(year)
        if month:
            query += ' AND MONTH(achievement_date) = %s'
            params.append(month)
        cursor.execute(query, tuple(params))
        achievements = cursor.fetchall()
        return jsonify(achievements)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_events', methods=['GET'])
def get_department_events():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # This would need to be implemented based on your events table structure
        # For now, returning empty array
        events = []
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_infrastructure', methods=['GET'])
def get_department_infrastructure():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # This would need to be implemented based on your infrastructure table structure
        # For now, returning empty array
        infrastructure = []
        return jsonify(infrastructure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# Department Profile API Endpoints with year/month filtering
@app.route('/get_department_laboratory', methods=['GET'])
def get_department_laboratory():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT id, lab_name, department, equipment_name, quantity, cost, 
                   purchase_date, company_name, specifications, remarks
            FROM laboratory_purchases
            WHERE department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(purchase_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(purchase_date) = %s"
            params.append(month)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_student_chapters', methods=['GET'])
def get_department_student_chapters():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT sc.id, sc.event_name, sc.start_date, sc.end_date, sc.venue, 
                   sc.resource_person, sc.college, sc.participant_count, sc.details,
                   GROUP_CONCAT(ed.department SEPARATOR ', ') AS departments
            FROM student_chapters sc
            LEFT JOIN event_departments ed ON sc.id = ed.event_id
            WHERE ed.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(sc.start_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(sc.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY sc.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_higher_education', methods=['GET'])
def get_department_higher_education():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT id, student_name, register_number, department, exam_type, 
                   exam_rank, exam_score, course, admitted_college, location, remarks
            FROM higher_education
            WHERE department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(created_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(created_date) = %s"
            params.append(month)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_internship', methods=['GET'])
def get_department_internship():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT id, student_name, register_number, department, allowed_year, 
                   company_name, company_details, start_date, end_date, duration, 
                   designation, stipend, mode, location, remarks
            FROM internship_opportunities
            WHERE department = %s
        '''
        params = [department]
        
        if year:
            query += " AND allowed_year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(start_date) = %s"
            params.append(month)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_alumni', methods=['GET'])
def get_department_alumni():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT id, alumni_name, talk_title, event_date, beneficiaries, 
                   alumni_job, alumni_regdno, company_details, department, 
                   participants, remarks
            FROM alumni_cell
            WHERE department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(event_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(event_date) = %s"
            params.append(month)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_mou', methods=['GET'])
def get_department_mou():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT id, university, contact_person, designation, start_date, 
                   end_date, mou_period, purpose, file_path, remarks
            FROM mou_academia
            WHERE 1=1
        '''
        params = []
        
        if year:
            query += " AND YEAR(start_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(start_date) = %s"
            params.append(month)
            
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_guest_speakers', methods=['GET'])
def get_department_guest_speakers():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT gs.id, gs.name, gs.designation, gs.visit_date, 
                   gs.purpose, gs.industry, gs.location, gs.remarks,
                   GROUP_CONCAT(DISTINCT gsd.department SEPARATOR ', ') AS departments
            FROM guest_speakers gs
            LEFT JOIN guest_speaker_departments gsd ON gs.id = gsd.guest_speaker_id
            WHERE gsd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(gs.visit_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(gs.visit_date) = %s"
            params.append(month)
            
        query += " GROUP BY gs.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_industrial_visits', methods=['GET'])
def get_department_industrial_visits():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT iv.visit_id as id, iv.industry_name, iv.start_date, iv.end_date, 
                   iv.location, iv.beneficiaries, iv.total_students, iv.remarks,
                   GROUP_CONCAT(DISTINCT ivd.department_name SEPARATOR ', ') AS departments
            FROM industrial_visits iv
            LEFT JOIN industrial_visit_departments ivd ON iv.visit_id = ivd.visit_id
            WHERE ivd.department_name = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(iv.start_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(iv.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY iv.visit_id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_hrd_fdp_sdp', methods=['GET'])
def get_department_hrd_fdp_sdp():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT e.id, e.event_title, e.event_type, e.start_date, e.start_time, 
                   e.end_date, e.end_time, e.convener_name, e.convener_phone, 
                   e.coordinator_name, e.coordinator_phone, e.resource_person, 
                   e.resource_person_designation, e.resource_person_cuo, e.topic, 
                   e.resource_person_details, e.beneficiaries, e.student_participants, 
                   e.remarks,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years
            FROM hrd_fdp_sdp_events e
            LEFT JOIN hrd_fdp_sdp_event_departments ed ON e.id = ed.event_id
            LEFT JOIN hrd_fdp_sdp_event_branches eb ON e.id = eb.event_id
            LEFT JOIN hrd_fdp_sdp_event_years ey ON e.id = ey.event_id
            WHERE ed.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND ey.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(e.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY e.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_conferences', methods=['GET'])
def get_department_conferences():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Try the simple table first
        try:
            query = '''
                SELECT id, conference_name, conference_type, start_date, end_date, 
                       venue, organized_by, department
                FROM conferences
                WHERE department = %s
            '''
            params = [department]
            
            if year:
                query += " AND YEAR(start_date) = %s"
                params.append(year)
            if month:
                query += " AND MONTH(start_date) = %s"
                params.append(month)
                
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            
            if data:
                # Convert timedelta to string if present
                for record in data:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)
                return jsonify(data)
        except:
            pass
        
        # If simple table doesn't work, try the complex structure
        query = '''
            SELECT c.id, c.event_title, c.conference_url, c.start_date, c.start_time, 
                   c.end_date, c.end_time, c.convener_name, c.convener_phone, 
                   c.treasurer_name, c.treasurer_phone, c.papers_received, 
                   c.papers_accepted, c.indexing, c.quartile_ranking, 
                   c.contact_email, c.contact_phone, c.remarks, c.brochure_path,
                   GROUP_CONCAT(cd.department SEPARATOR ', ') AS departments
            FROM conferences c
            LEFT JOIN conference_departments cd ON c.id = cd.conference_id
            WHERE cd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(c.start_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(c.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY c.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_workshops', methods=['GET'])
def get_department_workshops():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Try the simple table first
        try:
            query = '''
                SELECT id, event_name, event_type, start_date, end_date, 
                       venue, organized_by, department
                FROM workshops_seminars
                WHERE department = %s
            '''
            params = [department]
            
            if year:
                query += " AND YEAR(start_date) = %s"
                params.append(year)
            if month:
                query += " AND MONTH(start_date) = %s"
                params.append(month)
                
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            
            if data:
                # Convert timedelta to string if present
                for record in data:
                    for key, value in record.items():
                        if isinstance(value, timedelta):
                            record[key] = str(value)
                return jsonify(data)
        except:
            pass
        
        # If simple table doesn't work, try the complex structure
        query = '''
            SELECT w.id, w.event_name, w.national_international, w.event_type, 
                   w.start_date, w.end_date, w.topic, w.beneficiaries, 
                   w.student_participants, w.remarks,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years
            FROM workshops_seminars_guest_lectures w
            LEFT JOIN event_departments ed ON w.id = ed.event_id
            LEFT JOIN event_branches eb ON w.id = eb.event_id
            LEFT JOIN event_years ey ON w.id = ey.event_id
            WHERE ed.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND ey.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(w.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY w.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_hackathons', methods=['GET'])
def get_department_hackathons():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT h.id, h.hackathon_name, h.start_date, h.end_date, h.start_time, 
                   h.campus_allowed, h.team_limit, h.prize_details, h.winner_details, 
                   h.runner_details, h.second_runner_details, h.remarks, h.students_participated,
                   GROUP_CONCAT(DISTINCT hd.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT hy.year SEPARATOR ', ') AS years_allowed
            FROM hackathons h
            LEFT JOIN hackathon_departments hd ON h.id = hd.hackathon_id
            LEFT JOIN hackathon_years_allowed hy ON h.id = hy.hackathon_id
            WHERE hd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND hy.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(h.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY h.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_nss', methods=['GET'])
def get_department_nss():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT n.id, n.activity_name, n.start_date, n.end_date, n.start_time, 
                   n.purpose, n.coordinator_details, n.resource_person_details, 
                   n.remarks, n.students_participated,
                   GROUP_CONCAT(DISTINCT nya.year SEPARATOR ', ') AS years_allowed
            FROM nss_activities n
            LEFT JOIN nss_years_allowed nya ON n.id = nya.activity_id
            WHERE 1=1
        '''
        params = []
        
        if year:
            query += " AND nya.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(n.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY n.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_iic_iedc', methods=['GET'])
def get_department_iic_iedc():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT i.id, i.activity_name, i.start_date, i.end_date, i.students_participated, 
                   i.organizer_details, i.resource_person_details, i.significance, i.remarks,
                   GROUP_CONCAT(DISTINCT acb.conducted_by SEPARATOR ', ') AS conducted_by,
                   GROUP_CONCAT(DISTINCT aya.year SEPARATOR ', ') AS years_allowed
            FROM iic_iedc_msme_activities i
            LEFT JOIN activity_conducted_by acb ON i.id = acb.activity_id
            LEFT JOIN activity_years_allowed aya ON i.id = aya.activity_id
            WHERE 1=1
        '''
        params = []
        
        if year:
            query += " AND aya.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(i.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY i.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_engineers_day', methods=['GET'])
def get_department_engineers_day():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT e.id, e.event_name, e.event_date, e.students_participated, 
                   e.details, e.brochure_path,
                   GROUP_CONCAT(DISTINCT ed.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT eb.branch SEPARATOR ', ') AS branches,
                   GROUP_CONCAT(DISTINCT ey.year SEPARATOR ', ') AS years_allowed
            FROM engineers_day_events e
            LEFT JOIN engineers_day_departments ed ON e.id = ed.event_id
            LEFT JOIN engineers_day_branches eb ON e.id = eb.event_id
            LEFT JOIN event_years_allowed ey ON e.id = ey.event_id
            WHERE ed.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND ey.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(e.event_date) = %s"
            params.append(month)
            
        query += " GROUP BY e.id"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_ib_tech', methods=['GET'])
def get_department_ib_tech():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT i.id, i.activity_name, i.activity_type, i.start_date, i.end_date, 
                   i.coordinator_details, i.resource_person_details, 
                   i.students_participated, i.remarks,
                   GROUP_CONCAT(DISTINCT acd.department SEPARATOR ', ') AS conducted_departments
            FROM ibtech_activities i
            LEFT JOIN activity_conducted_departments acd ON i.id = acd.activity_id
            WHERE acd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND YEAR(i.start_date) = %s"
            params.append(year)
        if month:
            query += " AND MONTH(i.start_date) = %s"
            params.append(month)
            
        query += " GROUP BY i.id ORDER BY i.start_date DESC"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_parents_meetings', methods=['GET'])
def get_department_parents_meetings():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT p.id, p.purpose, p.meeting_date, p.meeting_time, p.venue, 
                   p.coordinator_details, p.parents_attended, p.remarks,
                   GROUP_CONCAT(DISTINCT mcd.department SEPARATOR ', ') AS conducted_departments,
                   GROUP_CONCAT(DISTINCT my.year SEPARATOR ', ') AS years
            FROM parents_meetings p
            LEFT JOIN meeting_conducted_departments mcd ON p.id = mcd.meeting_id
            LEFT JOIN meeting_years my ON p.id = my.meeting_id
            WHERE mcd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND my.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(p.meeting_date) = %s"
            params.append(month)
            
        query += " GROUP BY p.id ORDER BY p.meeting_date DESC"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_rd_events', methods=['GET'])
def get_department_rd_events():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT r.id, r.event_name, r.event_date, r.coordinator_details, 
                   r.resource_person_details, r.remarks, r.students_participated, r.brochure_path,
                   GROUP_CONCAT(DISTINCT red.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT rey.year SEPARATOR ', ') AS years_allowed
            FROM rd_events r
            LEFT JOIN rd_event_departments red ON r.id = red.event_id
            LEFT JOIN rd_event_years_allowed rey ON r.id = rey.event_id
            WHERE red.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND rey.year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(r.event_date) = %s"
            params.append(month)
            
        query += " GROUP BY r.id ORDER BY r.event_date DESC"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_department_fest_events', methods=['GET'])
def get_department_fest_events():
    department = request.args.get('department')
    year = request.args.get('year')
    month = request.args.get('month')
    
    if not department:
        return jsonify({"error": "Department name is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT f.id, f.fest_name, f.fest_date, f.fest_type, f.fest_significance, 
                   f.coordinator_details, f.resource_person_details, f.remarks, 
                   f.students_participated, f.brochure_path,
                   GROUP_CONCAT(DISTINCT fd.department SEPARATOR ', ') AS departments,
                   GROUP_CONCAT(DISTINCT fsy.student_year SEPARATOR ', ') AS student_years
            FROM fest_events f
            LEFT JOIN fest_departments fd ON f.id = fd.fest_id
            LEFT JOIN fest_student_years fsy ON f.id = fsy.fest_id
            WHERE fd.department = %s
        '''
        params = [department]
        
        if year:
            query += " AND fsy.student_year = %s"
            params.append(year)
        if month:
            query += " AND MONTH(f.fest_date) = %s"
            params.append(month)
            
        query += " GROUP BY f.id ORDER BY f.fest_date DESC"
        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        
        # Convert timedelta to string if present
        for record in data:
            for key, value in record.items():
                if isinstance(value, timedelta):
                    record[key] = str(value)

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/get_all_faculty_details', methods=['GET'])
def get_all_faculty_details():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT department, faculty_name, user_id FROM faculty_details order by department')
        records = cursor.fetchall()
        count = len(records)
        return jsonify({'count': count, 'records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# --- Dynamic Faculty Dropdown Endpoints ---
@app.route('/get_faculty_by_department')
def get_faculty_by_department():
    department = request.args.get('department')
    if not department:
        return jsonify([])
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM faculty_details WHERE department = %s", (department,))
    faculty_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(faculty_list)

@app.route('/get_faculty_name')
def get_faculty_name():
    faculty_id = request.args.get('faculty_id')
    department = request.args.get('department')
    if not faculty_id or not department:
        return jsonify({'faculty_name': ''})
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT faculty_name FROM faculty_details WHERE user_id = %s AND department = %s", (faculty_id, department))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'faculty_name': result['faculty_name'] if result else ''})

if __name__ == '__main__':
    app.run(debug=True)
