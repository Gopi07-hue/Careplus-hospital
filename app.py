import os
import sqlite3
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'careplus_hospital_secret_key_2026')
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                gender TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                specialization TEXT NOT NULL,
                experience TEXT DEFAULT '10+ Years',
                rating REAL DEFAULT 5.0,
                image_url TEXT,
                available_days TEXT DEFAULT 'Mon - Sat',
                available_time TEXT DEFAULT '09:00 AM - 05:00 PM',
                status TEXT DEFAULT 'Active'
            )
        ''')

        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                age INTEGER,
                phone TEXT NOT NULL,
                email TEXT,
                department TEXT NOT NULL,
                doctor_name TEXT,
                appointment_date TEXT NOT NULL,
                preferred_time TEXT NOT NULL,
                symptoms TEXT,
                status TEXT DEFAULT 'Confirmed',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Ambulance requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ambulance_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                location TEXT NOT NULL,
                emergency_type TEXT DEFAULT 'General Emergency',
                status TEXT DEFAULT 'Dispatched',
                eta_minutes INTEGER DEFAULT 8,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Blood bank table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blood_bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_group TEXT UNIQUE NOT NULL,
                units_available INTEGER NOT NULL DEFAULT 10,
                status TEXT DEFAULT 'Available',
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Contact messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                subject TEXT,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'Unread',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Hospital statistics & live status
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospital_stats (
                id INTEGER PRIMARY KEY,
                available_beds INTEGER DEFAULT 120,
                patients_waiting INTEGER DEFAULT 16,
                ambulances_ready INTEGER DEFAULT 8,
                happy_patients INTEGER DEFAULT 15000,
                doctors_count INTEGER DEFAULT 120,
                departments_count INTEGER DEFAULT 25,
                surgeries_count INTEGER DEFAULT 18500,
                awards_count INTEGER DEFAULT 45,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Pre-seed doctors if empty
        cursor.execute('SELECT COUNT(*) FROM doctors')
        if cursor.fetchone()[0] == 0:
            sample_doctors = [
                ('Dr. David Lee', 'Cardiology', 'Cardiologist', '14+ Years', 5.0, 
                 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=600&q=80',
                 'Mon - Fri', '09:00 AM - 04:00 PM'),
                ('Dr. Emily Brown', 'Pediatrics', 'Pediatrician', '10+ Years', 5.0,
                 'https://images.unsplash.com/photo-1594824813583-1e5b4cc60126?auto=format&fit=crop&w=600&q=80',
                 'Mon - Sat', '10:00 AM - 05:00 PM'),
                ('Dr. Michael Davis', 'General Surgery', 'General Surgeon', '16+ Years', 5.0,
                 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?auto=format&fit=crop&w=600&q=80',
                 'Tue - Sat', '08:30 AM - 03:30 PM'),
                ('Dr. John Smith', 'Cardiology', 'Senior Cardiologist', '18+ Years', 5.0,
                 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=600&q=80',
                 'Mon - Thu', '09:00 AM - 02:00 PM'),
                ('Dr. Sarah Johnson', 'Neurology', 'Neurologist', '12+ Years', 5.0,
                 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80',
                 'Wed - Sun', '11:00 AM - 06:00 PM')
            ]
            cursor.executemany('''
                INSERT INTO doctors (name, department, specialization, experience, rating, image_url, available_days, available_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_doctors)

        # Pre-seed blood bank if empty
        cursor.execute('SELECT COUNT(*) FROM blood_bank')
        if cursor.fetchone()[0] == 0:
            blood_groups = [
                ('A+', 24, 'Available'),
                ('B+', 18, 'Available'),
                ('O+', 32, 'Available'),
                ('AB+', 14, 'Available'),
                ('A-', 8, 'Low'),
                ('B-', 6, 'Low'),
                ('O-', 5, 'Critical'),
                ('AB-', 4, 'Critical')
            ]
            cursor.executemany('''
                INSERT INTO blood_bank (blood_group, units_available, status)
                VALUES (?, ?, ?)
            ''', blood_groups)

        # Pre-seed hospital stats if empty
        cursor.execute('SELECT COUNT(*) FROM hospital_stats')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO hospital_stats (id, available_beds, patients_waiting, ambulances_ready, 
                                            happy_patients, doctors_count, departments_count, 
                                            surgeries_count, awards_count)
                VALUES (1, 120, 16, 8, 15000, 120, 25, 18500, 45)
            ''')

        # Pre-seed sample appointments if empty
        cursor.execute('SELECT COUNT(*) FROM appointments')
        if cursor.fetchone()[0] == 0:
            sample_appointments = [
                ('Robert Vance', 48, '+91 9845123450', 'robert.v@example.com', 'Cardiology', 'Dr. David Lee', '2026-11-20', '10:30 AM', 'Routine cardiac follow-up and ECG check.', 'Confirmed'),
                ('Priya Sharma', 32, '+91 9765432101', 'priya.s@example.com', 'Neurology', 'Dr. Sarah Johnson', '2026-11-21', '02:00 PM', 'Persistent migraine episodes and vision aura.', 'Pending'),
                ('Marcus Aurel', 6, '+91 9811223344', 'm.aurel@example.com', 'Pediatrics', 'Dr. Emily Brown', '2026-11-22', '11:00 AM', 'Seasonal allergic cough and routine pediatric checkup.', 'Confirmed')
            ]
            cursor.executemany('''
                INSERT INTO appointments (patient_name, age, phone, email, department, doctor_name, appointment_date, preferred_time, symptoms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_appointments)

        # Pre-seed sample ambulance requests if empty
        cursor.execute('SELECT COUNT(*) FROM ambulance_requests')
        if cursor.fetchone()[0] == 0:
            sample_ambulances = [
                ('Alexander Cole', '+91 9822334455', 'Sector 14, Metro Avenue, City Center', 'Cardiac Emergency', 'Dispatched', 6),
                ('Meera Patel', '+91 9877665544', 'Greenwood Residency, Flat 402, North Road', 'Accident / Trauma', 'Arrived', 0)
            ]
            cursor.executemany('''
                INSERT INTO ambulance_requests (patient_name, phone, location, emergency_type, status, eta_minutes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_ambulances)

        conn.commit()


# Admin login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------ FRONTEND ROUTES ------------------ #

@app.route('/')
def index():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors WHERE status = "Active"')
        doctors = cursor.fetchall()

        cursor.execute('SELECT * FROM blood_bank ORDER BY id ASC')
        blood_bank = cursor.fetchall()

        cursor.execute('SELECT * FROM hospital_stats WHERE id = 1')
        stats = cursor.fetchone()

    return render_template('index.html', doctors=doctors, blood_bank=blood_bank, stats=stats)


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name', '').strip()
        age = request.form.get('age', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        doctor_name = request.form.get('doctor_name', '').strip()
        appointment_date = request.form.get('appointment_date', '').strip()
        preferred_time = request.form.get('preferred_time', '').strip()
        symptoms = request.form.get('symptoms', '').strip()

        if not patient_name or not phone or not department or not appointment_date:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('appointment'))

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (patient_name, age, phone, email, department, doctor_name, appointment_date, preferred_time, symptoms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed')
            ''', (patient_name, int(age) if age.isdigit() else None, phone, email, department, doctor_name, appointment_date, preferred_time, symptoms))
            conn.commit()

        flash('Your appointment has been booked successfully! Our coordinator will contact you shortly.', 'success')
        return redirect(url_for('appointment'))

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors WHERE status = "Active"')
        doctors = cursor.fetchall()

    return render_template('appointment.html', doctors=doctors)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill in your name, email, and message.', 'danger')
            return redirect(url_for('contact'))

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contact_messages (name, email, phone, subject, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, subject, message))
            conn.commit()

        flash('Thank you! Your message has been received. Our help desk will respond within 24 hours.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


# ------------------ API ENDPOINTS (AJAX) ------------------ #

@app.route('/api/book-appointment', methods=['POST'])
def api_book_appointment():
    try:
        data = request.get_json() or request.form
        patient_name = data.get('patient_name', '').strip()
        age = data.get('age', '')
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        department = data.get('department', '').strip()
        doctor_name = data.get('doctor_name', '').strip()
        appointment_date = data.get('appointment_date', '').strip()
        preferred_time = data.get('preferred_time', '').strip()
        symptoms = data.get('symptoms', '').strip()

        if not patient_name or not phone or not department or not appointment_date:
            return jsonify({'success': False, 'message': 'Please fill in all required fields (Name, Phone, Department, Date).'}), 400

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (patient_name, age, phone, email, department, doctor_name, appointment_date, preferred_time, symptoms, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Confirmed')
            ''', (patient_name, int(age) if str(age).isdigit() else None, phone, email, department, doctor_name, appointment_date, preferred_time, symptoms))
            booking_id = cursor.lastrowid
            conn.commit()

        return jsonify({
            'success': True,
            'booking_id': f'CP-{booking_id:05d}',
            'message': f'Appointment booked successfully for {patient_name} on {appointment_date} at {preferred_time}.',
            'data': {
                'id': booking_id,
                'name': patient_name,
                'department': department,
                'doctor': doctor_name,
                'date': appointment_date,
                'time': preferred_time
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/book-ambulance', methods=['POST'])
def api_book_ambulance():
    try:
        data = request.get_json() or request.form
        patient_name = data.get('patient_name', '').strip()
        phone = data.get('phone', '').strip()
        location = data.get('location', '').strip()
        emergency_type = data.get('emergency_type', 'General Emergency').strip()

        if not patient_name or not phone or not location:
            return jsonify({'success': False, 'message': 'Please provide Patient Name, Contact Phone, and Pickup Location.'}), 400

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ambulance_requests (patient_name, phone, location, emergency_type, status, eta_minutes)
                VALUES (?, ?, ?, ?, 'Dispatched', 8)
            ''', (patient_name, phone, location, emergency_type))
            request_id = cursor.lastrowid

            # Decrement ready ambulances safely
            cursor.execute('''
                UPDATE hospital_stats 
                SET ambulances_ready = CASE WHEN ambulances_ready > 0 THEN ambulances_ready - 1 ELSE 0 END
                WHERE id = 1
            ''')
            conn.commit()

        return jsonify({
            'success': True,
            'request_id': f'AMB-{request_id:04d}',
            'eta': '7 - 10 Minutes',
            'message': f'Ambulance dispatched to {location}. Driver contact: +91 98765 43210 (Demonstration Only).'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/live-status', methods=['GET'])
def api_live_status():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hospital_stats WHERE id = 1')
        stats = cursor.fetchone()

        stats_dict = {
            'available_beds': stats['available_beds'] if stats else 120,
            'patients_waiting': stats['patients_waiting'] if stats else 16,
            'ambulances_ready': stats['ambulances_ready'] if stats else 8,
            'current_time': datetime.now().strftime('%H:%M:%S')
        }
    return jsonify(stats_dict)


@app.route('/api/blood-bank', methods=['GET'])
def api_blood_bank():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blood_bank ORDER BY id ASC')
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
    return jsonify({'success': True, 'blood_bank': data})


@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.get_json() or {}
    user_msg = data.get('message', '').strip().lower()

    if not user_msg:
        return jsonify({'reply': 'Hello! I am CareBot, your CarePlus Hospital assistant. How can I assist you today? You can ask about doctor appointments, emergency ambulance, bed availability, blood bank stock, or departments.'})

    # Rule-based intelligent healthcare responses
    if any(k in user_msg for k in ['appointment', 'book', 'schedule', 'consult']):
        reply = 'You can book an appointment easily by clicking the "Book Appointment" button at the top, or visit our appointment section below. We have top specialists in Cardiology, Neurology, Pediatrics, and Surgery!'
    elif any(k in user_msg for k in ['ambulance', 'emergency', 'urgent', '108', 'accident']):
        reply = '🚨 For immediate medical emergency, please call our 24x7 Hotline at +91 9876543210 immediately, or use the "Book Ambulance" section on this page. Ambulances are equipped with ICU support.'
    elif any(k in user_msg for k in ['doctor', 'specialist', 'cardiologist', 'neurologist', 'surgeon']):
        reply = 'CarePlus has 120+ specialist doctors including Dr. David Lee & Dr. John Smith (Cardiology), Dr. Sarah Johnson (Neurology), Dr. Emily Brown (Pediatrics), and Dr. Michael Davis (General Surgery). You can review their full profiles in "Meet Our Specialists".'
    elif any(k in user_msg for k in ['blood', 'plasma', 'donor', 'a+', 'o+', 'b+']):
        reply = 'Our Blood Bank operates 24x7 with verified tested units for A+, B+, O+, AB+, and negative blood groups. Please scroll to the "Blood Bank Availability" section to view live unit counts.'
    elif any(k in user_msg for k in ['bed', 'icu', 'admit', 'waiting', 'live status']):
        reply = 'We currently have 120+ general and ICU beds available, with immediate admission for emergency and surgical care. Check the "Hospital Live Status" dashboard for live numbers.'
    elif any(k in user_msg for k in ['timing', 'hours', 'open', 'visit']):
        reply = 'Our Emergency, Trauma, ICU, and Pharmacy operate 24 hours a day, 7 days a week. OPD consultation hours are Monday through Saturday, 08:30 AM to 07:00 PM.'
    elif any(k in user_msg for k in ['location', 'address', 'where', 'map']):
        reply = 'CarePlus Hospital is centrally located at 100 Health Boulevard, Medical Enclave, City Center. Free ambulance parking and patient assistance are available at the main gate.'
    elif any(k in user_msg for k in ['insurance', 'cashless', 'tpa', 'claim']):
        reply = 'CarePlus provides 100% cashless treatment with over 40+ leading health insurance providers and government health schemes. Contact our TPA desk on the ground floor.'
    elif any(k in user_msg for k in ['hello', 'hi', 'hey', 'help']):
        reply = 'Hello! Welcome to CarePlus Hospital. I can assist you with Appointments, Emergency Ambulance, Doctor Availability, Blood Bank, and Visiting Hours. What would you like to know?'
    else:
        reply = 'Thank you for reaching out to CarePlus Hospital. For detailed medical guidance, please book an appointment with our specialist doctors or call our 24x7 reception desk at +91 9876543210.'

    return jsonify({'reply': reply})


# ------------------ ADMIN ROUTES ------------------ #

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Secure default demo credentials
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            session['admin_user'] = 'Admin'
            flash('Welcome back, Administrator!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid username or password. Default is admin / admin123'

    return render_template('admin_login.html', error=error)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    flash('You have logged out successfully.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin_dashboard():
    with get_db() as conn:
        cursor = conn.cursor()

        # Fetch appointments
        cursor.execute('SELECT * FROM appointments ORDER BY id DESC')
        appointments = cursor.fetchall()

        # Fetch ambulance requests
        cursor.execute('SELECT * FROM ambulance_requests ORDER BY id DESC')
        ambulance_requests = cursor.fetchall()

        # Fetch doctors
        cursor.execute('SELECT * FROM doctors ORDER BY id ASC')
        doctors = cursor.fetchall()

        # Fetch blood bank
        cursor.execute('SELECT * FROM blood_bank ORDER BY id ASC')
        blood_bank = cursor.fetchall()

        # Fetch contact messages
        cursor.execute('SELECT * FROM contact_messages ORDER BY id DESC')
        messages = cursor.fetchall()

        # Fetch stats
        cursor.execute('SELECT * FROM hospital_stats WHERE id = 1')
        stats = cursor.fetchone()

    return render_template(
        'admin.html',
        appointments=appointments,
        ambulance_requests=ambulance_requests,
        doctors=doctors,
        blood_bank=blood_bank,
        messages=messages,
        stats=stats
    )


@app.route('/admin/appointment/update-status/<int:id>', methods=['POST'])
@login_required
def admin_update_appointment_status(id):
    new_status = request.form.get('status', 'Confirmed')
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE appointments SET status = ? WHERE id = ?', (new_status, id))
        conn.commit()
    flash(f'Appointment #{id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/appointment/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_appointment(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (id,))
        conn.commit()
    flash(f'Appointment #{id} deleted successfully.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/ambulance/update-status/<int:id>', methods=['POST'])
@login_required
def admin_update_ambulance_status(id):
    new_status = request.form.get('status', 'Dispatched')
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE ambulance_requests SET status = ? WHERE id = ?', (new_status, id))
        conn.commit()
    flash(f'Ambulance request #{id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/blood-bank/update', methods=['POST'])
@login_required
def admin_update_blood_bank():
    blood_group = request.form.get('blood_group')
    units = request.form.get('units')

    if blood_group and units is not None:
        try:
            units = int(units)
            status = 'Available' if units >= 10 else ('Low' if units > 4 else 'Critical')
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE blood_bank 
                    SET units_available = ?, status = ?, last_updated = CURRENT_TIMESTAMP 
                    WHERE blood_group = ?
                ''', (units, status, blood_group))
                conn.commit()
            flash(f'Blood group {blood_group} units updated to {units} ({status}).', 'success')
        except ValueError:
            flash('Invalid unit count.', 'danger')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/doctor/add', methods=['POST'])
@login_required
def admin_add_doctor():
    name = request.form.get('name', '').strip()
    department = request.form.get('department', '').strip()
    specialization = request.form.get('specialization', '').strip()
    experience = request.form.get('experience', '5+ Years').strip()
    rating = request.form.get('rating', '5.0').strip()
    image_url = request.form.get('image_url', '').strip()

    if not image_url:
        image_url = 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80'

    if name and department and specialization:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO doctors (name, department, specialization, experience, rating, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, department, specialization, experience, float(rating) if rating else 5.0, image_url))
            conn.commit()
        flash(f'Doctor {name} added successfully.', 'success')
    else:
        flash('Please fill in doctor name, department, and specialization.', 'danger')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/doctor/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_doctor(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = ?', (id,))
        conn.commit()
    flash('Doctor removed successfully.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/stats/update', methods=['POST'])
@login_required
def admin_update_stats():
    beds = request.form.get('available_beds', 120)
    waiting = request.form.get('patients_waiting', 16)
    ambulances = request.form.get('ambulances_ready', 8)
    happy = request.form.get('happy_patients', 15000)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE hospital_stats 
            SET available_beds = ?, patients_waiting = ?, ambulances_ready = ?, happy_patients = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (int(beds), int(waiting), int(ambulances), int(happy)))
        conn.commit()
    flash('Hospital statistics updated successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    init_db()
    print("CarePlus Hospital server starting on http://127.0.0.1:5000 ...")
    app.run(debug=True, host='0.0.0.0', port=5000)
