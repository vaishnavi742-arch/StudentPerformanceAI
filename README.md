# 🎓 Student Performance AI

An AI-powered student performance and attendance analytics system built using Python, Streamlit, Pandas, Plotly, and Groq.

The application helps analyze student marksheets and attendance data through interactive dashboards and AI-assisted queries.

---

## 🚀 Features

### 📊 Student Performance Analysis

- Upload student marksheet data using Excel files
- View uploaded student records
- Calculate overall average marks
- Display total number of students
- Perform subject-wise performance analysis
- Analyze individual student performance
- Identify strongest and weakest subjects
- Analyze unit-wise marks
- Identify learning gaps
- Detect subjects requiring attention
- Identify failed subjects based on total marks

### 📅 Attendance Analysis

- Upload attendance data using Excel files
- Process and clean attendance records
- Analyze class attendance
- Perform subject-wise attendance analysis
- Analyze individual student attendance
- Identify students with attendance issues
- Query attendance information using the AI assistant

### 🤖 AI Academic Assistant

The system integrates the **Groq API** to provide AI-based responses about student academic performance and attendance.

Example questions:

- What is the student's overall performance?
- Which subject is the weakest?
- Which subject is the strongest?
- Did the student fail in any subject?
- Which unit is the weakest?
- Give me a performance summary.
- Who was absent on 2026-09-15?
- Which student has poor attendance?

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **Groq API**
- **Python-dotenv**
- **OpenPyXL**

---

## 📁 Project Structure

```text
StudentPerformanceAI/
│
├── app.py              # Main Streamlit application
├── marksheet.py        # Student performance analytics
├── attendance.py       # Attendance analytics
├── auth.py             # Authentication functionality
├── db.py               # Database-related functionality
├── utils.py             # Utility functions
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignored files
└── README.md           # Project documentation
