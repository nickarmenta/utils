import io
import os

import pandas as pd
import streamlit as st

from utils import process_contacts, process_visits

st.set_page_config(page_title="Report Parser", page_icon="📊", layout="wide")

st.title("📊 Report Parser")
st.markdown("Process spreadsheet reports for contacts and visits")

# Sidebar for report type selection
st.sidebar.header("Configuration")
report_type = st.sidebar.radio("Select Report Type", ["contacts", "visits"])

# Segmentation option for contacts
if report_type == "contacts":
    segment_contacts = st.sidebar.checkbox(
        "Segment into mailing lists",
        value=False,
        help="Split contacts into PNW, CA, and GG regions",
    )
else:
    segment_contacts = False

# File upload option
st.sidebar.header("Data Source")
use_upload = True 

if use_upload:
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel file", type=["xlsx", "xls"], key="file_upload"
    )

# Main processing area
if report_type == "contacts":
    st.header("Contacts Processing")
    st.markdown(
        """
    This processor will:
    - Remove all ID columns (UUIDs from database)
    - Combine Phone and Mobile into single Phone column
    - Parse Business Address into City, State, and Zip
    - Validate location data (invalid entries are cleared)
    - Filter to only include contacts from: WA, OR, CA, NM, NV, UT, CO, AZ, LA, TX, AR, WY, ID, MT, OK
    - Optional: Segment into three mailing lists (PNW, CA, GG)
    """
    )

    if use_upload:
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"Loaded {len(df)} rows from uploaded file")

                with st.expander("View Original Data (first 10 rows)"):
                    st.dataframe(df.head(10))

                if st.button("Process Contacts", type="primary"):
                    with st.spinner("Processing..."):
                        result = process_contacts(
                            df, segment_by_region=segment_contacts
                        )

                    if segment_contacts:
                        st.success(
                            f"Processing complete! Segmented into {len(result)} mailing lists"
                        )

                        # Show summary for each region
                        for region_name, region_df in result.items():
                            st.subheader(f"{region_name} Region")
                            st.info(f"{len(region_df)} contacts")

                            with st.expander(
                                f"View {region_name} Data (first 20 rows)"
                            ):
                                st.dataframe(region_df.head(20))

                            # Download button for each region
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                                region_df.to_excel(writer, index=False)
                            output.seek(0)

                            st.download_button(
                                label=f"Download {region_name} List",
                                data=output,
                                file_name=f"Contact_{region_name}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_upload_{region_name}",
                            )
                    else:
                        st.success(
                            f"Processing complete! {len(result)} contacts processed"
                        )

                        with st.expander("View Processed Data (first 20 rows)"):
                            st.dataframe(result.head(20))

                        # Download button
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine="openpyxl") as writer:
                            result.to_excel(writer, index=False)
                        output.seek(0)

                        st.download_button(
                            label="Download Processed File",
                            data=output,
                            file_name="Contact_Processed.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        else:
            st.info("Please upload a Contact Excel file to begin")

elif report_type == "visits":
    st.header("Visits Processing")
    st.markdown(
        """
    This processor will:
    - Remove unnecessary columns (ID, Status, Technical IDs, etc.)
    - Clean and format visit data
    """
    )

    if use_upload:
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"Loaded {len(df)} rows from uploaded file")

                with st.expander("View Original Data (first 10 rows)"):
                    st.dataframe(df.head(10))

                if st.button("Process Visits", type="primary"):
                    with st.spinner("Processing..."):
                        processed_df = process_visits(df)

                    st.success(
                        f"Processing complete! {len(processed_df)} visits processed"
                    )

                    with st.expander("View Processed Data (first 20 rows)"):
                        st.dataframe(processed_df.head(20))

                    # Download button
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        processed_df.to_excel(writer, index=False)
                    output.seek(0)

                    st.download_button(
                        label="Download Processed File",
                        data=output,
                        file_name="Visit_Processed.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        else:
            st.info("Please upload a Visit Excel file to begin")
