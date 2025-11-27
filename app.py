{\rtf1\ansi\ansicpg936\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from spellchecker import SpellChecker\
\
# -------------------------------\
#   App Header & Description\
# -------------------------------\
st.title("
\f1 \uc0\u55357 \u56536 
\f0  Spelling Counter \'96 Streamlit Version")\
st.write("""\
This web application is **converted from my previously submitted Jupyter Notebook:  \
`spelling_counter_modified.ipynb`**.\
\
The original notebook performed the following tasks:\
\
- Load multiple `.txt` files  \
- Detect misspelled words using **pyspellchecker**  \
- Count the frequency of each misspelled word  \
- Output the results in CSV format  \
\
This Streamlit version fully reproduces the same logic \
but provides an interactive web interface for easier use.\
""")\
\
st.markdown("---")\
\
# -------------------------------\
#   Spell Checker Functionality\
# -------------------------------\
st.header("
\f1 \uc0\u55357 \u56541 
\f0  Upload TXT Files for Spell Checking")\
\
uploaded_files = st.file_uploader(\
    "Upload one or more .txt files:",\
    type=["txt"],\
    accept_multiple_files=True\
)\
\
spell = SpellChecker()\
\
if uploaded_files:\
    st.success(f"\{len(uploaded_files)\} file(s) uploaded successfully!")\
\
    results = []\
\
    for file in uploaded_files:\
        text = file.read().decode("utf-8", errors="ignore")\
        words = text.split()\
\
        # find misspelled words\
        misspelled = spell.unknown(words)\
        freq = \{\}\
\
        for w in words:\
            if w in misspelled:\
                freq[w] = freq.get(w, 0) + 1\
\
        df = pd.DataFrame(\{\
            "misspelled_word": list(freq.keys()),\
            "frequency": list(freq.values())\
        \}).sort_values("frequency", ascending=False)\
\
        st.subheader(f"
\f1 \uc0\u55357 \u56589 
\f0  Misspelled Words in: `\{file.name\}`")\
        st.dataframe(df)\
\
        df["filename"] = file.name\
        results.append(df)\
\
    if results:\
        final_df = pd.concat(results, ignore_index=True)\
\
        st.markdown("### 
\f1 \uc0\u55357 \u56549 
\f0  Download All Results as CSV")\
        csv_data = final_df.to_csv(index=False).encode("utf-8")\
        st.download_button(\
            label="Download Spelling Results CSV",\
            data=csv_data,\
            file_name="spelling_results.csv",\
            mime="text/csv"\
        )\
\
}