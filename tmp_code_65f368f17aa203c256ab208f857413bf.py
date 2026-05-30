from db_config import connect_db

def setup_university_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("DROP TABLE IF EXISTS students, courses, departments")
    
    cursor.execute("""
        CREATE TABLE departments (
            dept_id INT PRIMARY KEY AUTO_INCREMENT,
            dept_name VARCHAR(100) UNIQUE NOT NULL,
            building VARCHAR(50) NOT NULL,
            budget DECIMAL(12,2) CHECK (budget > 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE courses (
            course_id VARCHAR(10) PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            credits INT CHECK (credits BETWEEN 1 AND 5),
            dept_id INT,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE students (
            student_id INT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15) NOT NULL,
            enroll_date DATE DEFAULT (CURRENT_DATE),
            dept_id INT,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    # Insert Data
    cursor.executemany("INSERT INTO departments VALUES (%s, %s, %s, %s)", [
        (101, 'Computer Science & Engineering', 'Ramanujan Block', 1500000.00),
        (102, 'Mechanical Engineering', 'Kalam Labs', 1200000.00),
        (103, 'Electrical & Electronics', 'Tesla Pavilion', 950000.00),
        (104, 'Business Administration', 'Aryabhata Hall', 800000.00)
    ])

    cursor.executemany("INSERT INTO courses VALUES (%s, %s, %s, %s)", [
        ('CS101', 'Introduction to Python', 4, 101),
        ('CS202', 'Database Management Systems', 4, 101),
        ('ME105', 'Engineering Graphics', 3, 102),
        ('EE210', 'Circuit Theory', 4, 103),
        ('BA101', 'Principles of Management', 3, 104)
    ])

    cursor.executemany("INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)", [
        (2026001, 'Sairam', 'Krishnan', 'sairam.k@univ.edu', '9876543210', '2026-06-01', 101),
        (2026002, 'Abami', 'Priya', 'abami.p@univ.edu', '9876543211', '2026-06-01', 101),
        (2026003, 'Rahul', 'Sharma', 'rahul.s@univ.edu', '9876543212', '2026-06-02', 102),
        (2026004, 'Meera', 'Nair', 'meera.n@univ.edu', '9876543213', '2026-06-03', 103),
        (2026005, 'Vikram', 'Singh', 'vikram.s@univ.edu', '9876543214', '2026-06-05', 104)
    ])

    conn.commit()
    cursor.close()
    conn.close()

setup_university_db()