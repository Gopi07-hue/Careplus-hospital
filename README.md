# CarePlus Hospital – Modern Responsive Hospital Website

A complete, modern, responsive hospital website and healthcare management system for **CarePlus Hospital**, engineered with **Python Flask**, **SQLite**, and **HTML5/CSS3/JavaScript**.

---

## 🌟 Key Features

1. **Top Information Bar**:
   - Hospital Hotline: `+91 9876543210`
   - Email: `careplus@hospital.com`
   - 24×7 Emergency badge & NABH Accreditation info.

2. **Fixed Header & Navigation**:
   - CarePlus branding with modern logo icon.
   - Smooth navigation: Home, Services, Departments, Doctors, Gallery, Appointment, Contact.
   - **Dark Mode & Light Mode** toggle button with localStorage theme memory.
   - Mobile responsive navigation drawer.

3. **Hero Section & Emergency Banner**:
   - Hero header: *"Advanced Healthcare For Everyone"*.
   - Subtitle: *"World-Class Doctors • Smart Technology • 24×7 Emergency Care • Compassionate Treatment"*.
   - Call-to-actions: `[ Book Appointment ]` and `[ Explore Services ]`.
   - Colorful Emergency ribbon showing hotline, 24×7 availability, 120+ specialists, and fast ambulance dispatch.

4. **Our Premium Services**:
   - 8 specialized cards: Pulmonology, General Medicine, Cardiology, Neurology, Orthopedics, Pediatrics, Laboratory Services, Pharmacy.

5. **Quick Access**:
   - 6 interactive cards: Book Appointment, Lab Reports, Online Pharmacy, Emergency, Medical Records, Health Insurance.

6. **Hospital Statistics**:
   - Blue gradient banner with animated counting numbers:
     - 15,000+ Happy Patients
     - 120+ Doctors
     - 25+ Departments
     - 18,500+ Successful Surgeries
     - 45+ Awards

7. **Why Patients Trust Us**:
   - 4 feature cards: 25+ Years Experience, 15,000+ Happy Patients, Modern Equipment, 24×7 Support.

8. **Meet Our Specialists**:
   - Horizontal doctor cards with professional photographs, credentials, ratings (★★★★★), and quick consultation booking.
   - Pre-seeded with: Dr. David Lee, Dr. Emily Brown, Dr. Michael Davis, Dr. John Smith, and Dr. Sarah Johnson.

9. **Our Departments**:
   - 4 large blue-gradient department cards: Cardiology ❤️, Neurology 🧠, Orthopedics 🦴, Pediatrics 👶.

10. **Hospital Journey**:
    - Milestone timeline: 1998 (Founded) → 2007 (ICU Started) → 2015 (NABH Certified) → 2022 (Robotic Surgery) → 2026 (AI Healthcare).

11. **Hospital Gallery**:
    - Responsive image grid with hover zoom and interactive Lightbox modal (Reception, Patient Wards, Diagnostics, Pharmacy, Doctors & Equipment).

12. **Health Calculator**:
    - **BMI Calculator**: Calculates Body Mass Index and displays health category with actionable feedback.
    - **Heart Rate Status**: Checks resting pulse rate with educational guidelines.

13. **Hospital Live Status**:
    - Live facility metrics: Available Beds, Patients Waiting, Ambulances Ready, and an automatically ticking real-time digital clock.

14. **Blood Bank Availability**:
    - Cards for all major blood groups: A+, B+, O+, AB+, A-, B-, O-, AB- with unit stocks and status badges (*Available, Low, Critical*).

15. **Health Tips**:
    - Auto-rotating wellness carousel with guidance on hydration, cardiovascular health, sleep, nutrition, and mental balance.

16. **Book Ambulance**:
    - Emergency form storing requests in the database and providing instant booking confirmation with ETA and dispatch details.

17. **Appointment Booking**:
    - Complete booking form with validation, department & doctor selection, slot booking, and database storage.

18. **Floating Utilities & AI Assistant**:
    - Bottom-left floating **CareBot AI Assistant** answering patient queries interactively.
    - Right-side vertical quick action buttons (Appointment, Gallery, Hotline, Tips).
    - Back-to-Top button with smooth scrolling.

19. **Admin Dashboard (`/admin`)**:
    - Secure login (`admin` / `admin123`).
    - View and filter patient appointments, update status (*Confirmed, Completed, Cancelled*), or delete.
    - Track emergency ambulance requests and change dispatch status.
    - Live Blood Bank stock editor with one-click unit adjustments.
    - Doctor roster management (Add/Remove specialists).
    - Hospital live status editor (update beds, waiting count, ambulances).
    - View incoming contact inquiries.

---

## 📁 Project Structure

```text
careplus-hospital/
│
├── app.py                      # Flask backend, database initialization & REST APIs
├── database.db                 # SQLite database (auto-created on startup)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation and run instructions
│
├── templates/
│   ├── index.html              # Main hospital website
│   ├── appointment.html        # Dedicated appointment booking page
│   ├── contact.html            # Dedicated contact page
│   ├── admin_login.html        # Staff and admin login portal
│   └── admin.html              # Hospital administration dashboard
│
└── static/
    ├── css/
    │   └── style.css           # Modern styles, gradients, dark/light theme variables
    ├── js/
    │   └── script.js           # Calculators, counters, clock, AJAX forms, chatbot & theme toggle
    └── images/                 # Local image assets
```

---

## 🚀 How to Run Locally

### 1. Requirements
- Python 3.8+ installed on your computer.

### 2. Install Dependencies
Open your terminal in the `careplus-hospital` directory:

```bash
cd careplus-hospital
pip install -r requirements.txt
```

### 3. Start the Application
Run:

```bash
python app.py
```

### 4. Access the Website
Open your browser and navigate to:
- **Main Website**: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- **Book Appointment**: [http://127.0.0.1:5000/appointment](http://127.0.0.1:5000/appointment)
- **Contact Us**: [http://127.0.0.1:5000/contact](http://127.0.0.1:5000/contact)
- **Admin Portal**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

### 5. Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛠️ Technology Stack
- **Backend**: Python Flask 3.x
- **Database**: SQLite3
- **Frontend**: Semantic HTML5, CSS3 (CSS Variables, Flexbox, CSS Grid), Vanilla JavaScript (ES6+)
- **Design Tokens**: Primary Blue `#087BFA`, Cyan `#00BCD4`, Light Blue `#EEF7FF`, Poppins Font, Font Awesome 6.5.
