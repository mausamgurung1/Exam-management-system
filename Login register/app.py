import streamlit as st
import pandas as pd
import io

st.title("Internal Marks Admin Panel")

# Upload CSV
uploaded_file = st.file_uploader("Upload Internal Marks CSV", type=["csv"])

if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file)
    st.success("CSV loaded successfully.")

    # Display DataFrame
    st.subheader("Current Marks Data")
    st.dataframe(df)

    # Select student row
    student_selector = st.selectbox("Select a student to edit", df.index, format_func=lambda i: f"{df.loc[i, 'Student Name']} (ID: {df.loc[i, 'Student ID']})")

    # Select subject column to edit
    mark_column = st.selectbox("Select column to edit", [col for col in df.columns if "Obtained" in col or "Marks" in col])

    # Input new value
    new_value = st.number_input(f"Enter new value for {mark_column}", min_value=0.0, step=0.5)

    # Update button
    if st.button("Update Marks"):
        df.at[student_selector, mark_column] = new_value
        st.success(f"Updated {mark_column} for {df.loc[student_selector, 'Student Name']}")

    # Download updated CSV
    st.subheader("Download Updated File")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, file_name="Updated_Internal_Marks.csv", mime='text/csv')
