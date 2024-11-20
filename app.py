import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection
MONGO_URI = "mongodb+srv://soumyajitjalua1:Soumyajit%402024@cluster0.xxvdt.mongodb.net"
client = MongoClient(MONGO_URI)
db = client['NLP_project']  # Replace with your database name
collection = db['CSV_data']  # Replace with your collection name

# Streamlit App
st.title("CVE Information Fetcher")

# Input: CVE ID
cve_id = st.text_input("Enter CVE ID", placeholder="e.g., CVE-1999-0001")

if st.button("Fetch Data"):
    if not cve_id:
        st.error("Please enter a CVE ID.")
    else:
        # Fetch data from MongoDB
        cve_data = collection.find_one({"id": cve_id})
        
        if not cve_data:
            st.error("No data found for the given CVE ID.")
        else:
            # Display CVE details
            st.write("### CVE Details:")
            st.json(cve_data)

            # Convert references to a DataFrame for better display
            if "references" in cve_data and cve_data["references"]:
                st.write("### References:")
                references_df = pd.DataFrame(cve_data["references"], columns=["URL"])
                st.dataframe(references_df)

            # Highlight key information
            st.write("### Key Impact Details:")
            st.write(f"- **Confidentiality Impact**: {cve_data.get('confidentialityImpact', 'N/A')}")
            st.write(f"- **Integrity Impact**: {cve_data.get('integrityImpact', 'N/A')}")
            st.write(f"- **Availability Impact**: {cve_data.get('availabilityImpact', 'N/A')}")

            # Include CVSS score and severity
            st.write(f"- **CVSS Score**: {cve_data.get('cvssScore', 'N/A')}")
            st.write(f"- **Access Complexity**: {cve_data.get('accessComplexity', 'N/A')}")
            st.write(f"- **Authentication Required**: {cve_data.get('authenticationRequired', 'N/A')}")
