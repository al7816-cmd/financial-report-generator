import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.title("Heartbeat Cohort Processor")

st.write("Upload your Excel file to process it.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    # Read uploaded file into pandas (no saving to disk)
    df = pd.read_excel(uploaded_file, header=4)

    months = [
        '2025-04-01','2025-05-01','2025-06-01','2025-07-01',
        '2025-08-01','2025-09-01','2025-10-01','2025-11-01',
        '2025-12-01','2026-01-01'
    ]

    heartbeat_cohorted = pd.DataFrame(
        index=months,
        columns=[
            'cohort_size','month_0','month_1','month_2','month_3',
            'month_4','month_5','month_6','month_7','month_8','month_9'
        ]
    )

    # Convert column names to string format
    df.columns = df.columns.map(
        lambda x: x.strftime("%Y-%m-%d") if hasattr(x, "strftime") else str(x)
    )

    # Process data
    for month in months:
        heartbeat_cohorted.loc[month, 'cohort_size'] = df[
            df['Unnamed: 1'] == 'New Successful Onboarding Users (Heartbeat)'
        ][month].iloc[0]

    heartbeat_cohorted['month_0'] = heartbeat_cohorted['cohort_size']

    st.success("Processing complete!")

    # Create in-memory Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        heartbeat_cohorted.to_excel(writer)

    output.seek(0)

    st.download_button(
        label="Download Processed File",
        data=output,
        file_name="heartbeat_cohorted_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )