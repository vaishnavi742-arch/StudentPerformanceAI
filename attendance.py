def run():

    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from groq import Groq
    from dotenv import load_dotenv
    import os
    import re

    # =====================================
    # LOAD ENV
    # =====================================
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # =====================================
    # DATA PROCESSING
    # =====================================
    def process_attendance_file(df):
        df.columns = df.columns.str.strip()

        df.rename(columns={
            "Student Name": "Student",
            "Register Number": "RegNo"
        }, inplace=True)

        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        return df

    def clean_attendance(df):
        df["Status"] = df["Status"].astype(str).str.upper()

        df["Status"] = df["Status"].replace({
            "PRESENT": "P",
            "ABSENT": "AB",
            "A": "AB"
        })

        return df

    # =====================================
    # SMART QUERY
    # =====================================
    def smart_query(df, question):
        q = question.lower()

        if "absent" in q and "on" in q:
            match = re.search(r"\d{4}-\d{2}-\d{2}", q)

            if not match:
                return "Use date format YYYY-MM-DD", None

            date = pd.to_datetime(match.group()).date()

            filtered = df[
                (df["Date"] == date) &
                (df["Status"] == "AB")
            ]

            # subject filter
            if "Subject" in df.columns:
                for sub in df["Subject"].unique():
                    if sub.lower() in q:
                        filtered = filtered[
                            filtered["Subject"].str.lower() == sub.lower()
                        ]

            if filtered.empty:
                return "No absentees found", None

            result = filtered[["Student", "RegNo"]].drop_duplicates()

            return f"Absentees on {date}", result

        # fallback AI
        data_text = df.to_string(index=False)

        prompt = f"""
Use only given data.

Data:
{data_text}

Question:
{question}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content, None

    # =====================================
    # UI START
    # =====================================
    st.title("📊 AI Attendance Dashboard")

    uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

    if uploaded_file:

        df = pd.read_excel(uploaded_file)
        df = process_attendance_file(df)
        df = clean_attendance(df)

        st.subheader("📋 Data")
        st.dataframe(df, use_container_width=True)

        # =====================================
        # CLASS GRAPH
        # =====================================
        st.subheader("📊 Class Attendance %")

        overall = (
            df.groupby("Student")["Status"]
            .value_counts()
            .unstack(fill_value=0)
        )

        overall["Attendance %"] = round(
            overall["P"] / (overall["P"] + overall["AB"]) * 100, 2
        )

        fig_class = px.bar(
            overall.reset_index(),
            x="Student",
            y="Attendance %",
            title="Overall Attendance Percentage"
        )

        st.plotly_chart(fig_class, use_container_width=True)

        # =====================================
        # SUBJECT GRAPH
        # =====================================
        if "Subject" in df.columns:

            st.subheader("📚 Subject-wise Attendance")

            subject_summary = (
                df.groupby(["Subject", "Status"])
                .size()
                .reset_index(name="Count")
            )

            fig_subject = px.bar(
                subject_summary,
                x="Subject",
                y="Count",
                color="Status",
                barmode="group"
            )

            st.plotly_chart(fig_subject, use_container_width=True)

        # =====================================
        # STUDENT ANALYSIS
        # =====================================
        st.subheader("🎓 Student Analysis")

        student = st.selectbox("Select Student", sorted(df["Student"].unique()))
        student_df = df[df["Student"] == student]

        present = len(student_df[student_df["Status"] == "P"])
        absent = len(student_df[student_df["Status"] == "AB"])
        total = present + absent
        percent = round((present / total) * 100, 2) if total else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric("Present", present)
        col3.metric("Absent", absent)
        col4.metric("%", f"{percent}%")

        fig_student = px.pie(
            values=[present, absent],
            names=["Present", "Absent"],
            title=f"{student} Attendance"
        )

        st.plotly_chart(fig_student, use_container_width=True)

        # =====================================
        # AI SECTION
        # =====================================
        st.subheader("🤖 AI Assistant")

        question = st.text_input("Ask question...")

        if st.button("Get Answer"):

            if question.strip():

                title, result = smart_query(df, question)

                st.markdown(f"### {title}")

                if isinstance(result, pd.DataFrame):
                    st.dataframe(result, use_container_width=True)
                else:
                    st.info(title)

            else:
                st.warning("Enter a question")

    else:
        st.info("Upload file to start")