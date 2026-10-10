import streamlit as st
from database import add_student, get_students, get_student
from services import calculate_grade, calculate_statistics

st.title("🎓 Student Performance Dashboard")

# 1. Student əlavə etmək forması
st.subheader("Yeni Tələbə Əlavə Et")
with st.form("student_form"):
    student_name = st.text_input("Student Name")
    student_score = st.number_input("Score", min_value=0, max_value=100, step=1)
    submit_button = st.form_submit_button("Add Student")

    if submit_button:
        if student_name.strip() != "":
            add_student(student_name, int(student_score))
            st.success(f"'{student_name}' uğurla əlavə olundu!")
            st.rerun()
        else:
            st.warning("Zəhmət olmasa tələbənin adını daxil edin.")

st.divider()

# 3. Student axtarışı
st.subheader("Tələbə Axtarışı")
search_query = st.text_input("Search Student [____________]")

if search_query:
    students_data = get_student(search_query)
else:
    students_data = get_students()

# 2. Student siyahısını göstərmək və Grade əlavə etmək
st.subheader("Tələbələrin Siyahısı")
if students_data:
    formatted_data = []
    for s in students_data:
        formatted_data.append({
            "Name": s["Name"],
            "Score": s["Score"],
            "Grade": calculate_grade(s["Score"])
        })

    st.dataframe(formatted_data, use_container_width=True)

    # 4. Statistikalar
    st.subheader("Statistikalar")
    stats = calculate_statistics(students_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", stats["total"])
    col2.metric("Average Score", stats["average"])
    col3.metric("Highest Score", stats["highest"])
    col4.metric("Lowest Score", stats["lowest"])
else:
    st.info("Heç bir tələbə tapılmadı.")