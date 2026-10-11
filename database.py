import sqlite3
import pyodbc
from config import DB_DRIVER, DB_NAME, DB_SERVER


def get_sqlite_connection():
    conn = sqlite3.connect("university.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Students (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Score REAL NOT NULL
        )
    """
    )
    cursor.execute("SELECT COUNT(*) FROM Students")
    if cursor.fetchone()[0] == 0:
        sample_students = [
            ("Ali", 85),
            ("Leyla", 72),
            ("Murad", 48),
            ("Aysel", 91),
            ("Kamran", 63),
        ]
        cursor.executemany(
            "INSERT INTO Students (Name, Score) VALUES (?, ?)", sample_students
        )
    conn.commit()
    return conn


def create_connection():
    try:
        connection_string = (
            f"DRIVER={DB_DRIVER};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_connection=yes;"
        )
        conn = pyodbc.connect(connection_string, timeout=2)
        return ("odbc", conn)
    except Exception:
        return ("sqlite", get_sqlite_connection())


def add_student(name: str, score: int):
    db_type, conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Students (Name, Score) VALUES (?, ?)", (name, score)
        )
        conn.commit()
        cursor.close()
        conn.close()


def get_students():
    db_type, conn = create_connection()
    students = []
    if conn:
        cursor = conn.cursor()
        if db_type == "odbc":
            cursor.execute("EXEC GetStudentResult")
            rows = cursor.fetchall()
            students = [{"Name": row.Name, "Score": row.Score} for row in rows]
        else:
            cursor.execute("SELECT Name, Score FROM Students")
            rows = cursor.fetchall()
            students = [{"Name": row[0], "Score": row[1]} for row in rows]
        cursor.close()
        conn.close()
    return students


def get_student(search_name: str):
    db_type, conn = create_connection()
    students = []
    if conn:
        cursor = conn.cursor()
        if db_type == "odbc":
            cursor.execute(
                "EXEC GetStudentResult @StudentName = ?", (search_name,)
            )
            rows = cursor.fetchall()
            students = [{"Name": row.Name, "Score": row.Score} for row in rows]
        else:
            cursor.execute(
                "SELECT Name, Score FROM Students WHERE Name LIKE ?",
                (f"%{search_name}%",),
            )
            rows = cursor.fetchall()
            students = [{"Name": row[0], "Score": row[1]} for row in rows]
        cursor.close()
        conn.close()
    return students
