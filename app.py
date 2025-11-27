import streamlit as st
import pandas as pd
from spellchecker import SpellChecker

# -------------------------------
#   App Header & Description
# -------------------------------
st.title("📘 Spelling Counter – Streamlit Version")
st.write("""
This web application is **converted from my previously submitted Jupyter Notebook:  
`spelling_counter_modified.ipynb`**.

The original notebook performed the following tasks:

- Load multiple `.txt` files  
- Detect misspelled words using **pyspellchecker**  
- Count the frequency of each misspelled word  
- Output the results in CSV format  

This Streamlit version fully reproduces the same logic 
but provides an interactive web interface for easier use.
""")

st.markdown("---")

# -------------------------------
#   Spell Checker Functionality
# -------------------------------
st.header("📝 Upload TXT Files for Spell Checking")

uploaded_files = st.file_uploader(
    "Upload one or more .txt files:",
    type=["txt"],
    accept_multiple_files=True
)

spell = SpellChecker()

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")

    results = []

    for file in uploaded_files:
        text = file.read().decode("utf-8", errors="ignore")
        words = text.split()

        # find misspelled words
        misspelled = spell.unknown(words)
        freq = {}

        for w in words:
            if w in misspelled:
                freq[w] = freq.get(w, 0) + 1

        df = pd.DataFrame({
            "misspelled_word": list(freq.keys()),
            "frequency": list(freq.values())
        }).sort_values("frequency", ascending=False)

        st.subheader(f"🔍 Misspelled Words in: `{file.name}`")
        st.dataframe(df)

        df["filename"] = file.name
        results.append(df)

    if results:
        final_df = pd.concat(results, ignore_index=True)

        st.markdown("### 📥 Download All Results as CSV")
        csv_data = final_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Spelling Results CSV",
            data=csv_data,
            file_name="spelling_results.csv",
            mime="text/csv"
        )

