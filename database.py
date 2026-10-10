import pyodbc
from config import DB_SERVER, DB_NAME, DB_DRIVER

def create_connection():
    """SQL Server ilə əlaqə yaradır."""
    connection_string = (
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"Trusted_connection=yes;"
    )
    return pyodbc.connect(connection_string)

def add_student(name: str, score: int):
    """Verilənlər bazasına yeni tələbə əlavə edir."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (Name, Score) VALUES (?, ?)", (name, score))
    conn.commit()
    cursor.close()
    conn.close()

def get_students():
    """Bütün tələbələrin siyahısını bazadan çəkir."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC GetStudentResult")
    rows = cursor.fetchall()

    students = [{"Name": row.Name, "Score": row.Score} for row in rows]
    cursor.close()
    conn.close()
    return students

def get_student(search_name: str):
    """Ada görə tələbə axtarışı edir."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC GetStudentResult @StudentName = ?", (search_name,))
    rows = cursor.fetchall()

    students = [{"Name": row.Name, "Score": row.Score} for row in rows]
    cursor.close()
    conn.close()
    return students