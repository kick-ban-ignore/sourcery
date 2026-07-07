import streamlit as st
import pandas as pd

###
### "Sourcery" - your little helper when dealing with scientific sources when writing your PhD thesis. 
### Sourcery is a minimalistic Streamlit web application that allows users to upload CSV files containing source data
### (like research papers or references) and filter and explore the data. 
###


# Page Config
st.set_page_config(page_title="Sourcery - Quellenübersicht", layout="wide")

# Title
st.sidebar.markdown("<h1 style='font-size: 5rem;'>\U0001F426</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 20px;'>Sourcery - Quellenübersicht</p>", unsafe_allow_html=True)

# File upload in sidebar
uploaded_file = st.sidebar.file_uploader("CSV-Datei hochladen", type=["csv"])

if uploaded_file is not None:
    # Check if the uploaded file is ok
    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Datei: {e}")
        st.stop()

    # Clean column names in dataframe
    df.columns = df.columns.str.strip()

    # Main content
    st.title("Quellenübersicht")
    st.write("Hier werden die gefilterten Quellen angezeigt:")

    # --- TAB: filters 
    st.sidebar.header('Einstellungen')
    
    column_options = df.columns.tolist()
    
    # 1. Freeze columns
    # Standard: "Titel", "Autoren" if exists
    default_freeze = [col for col in ["Titel", "Autoren"] if col in column_options]
    frozen_cols = st.sidebar.multiselect(
        "Spalten fixieren:",
        options=column_options,
        default=default_freeze
    )

    st.sidebar.markdown("---")
    st.sidebar.header('Filter')
    
    # 2. Which columns to filter
    desired_defaults = ["Autoren", "Studientyp", "Diagnose (ICD)"]
    valid_defaults = [col for col in desired_defaults if col in column_options]
    if not valid_defaults and len(column_options) > 0:
        valid_defaults = column_options[:3]

    selected_filters = st.sidebar.multiselect(
        "Welche Spalten möchtest du filtern?",
        options=column_options,
        default=valid_defaults
    )

    # Create filter dictionary dynamically
    filter_dict = {}  
    for col in selected_filters:
        unique_values = df[col].dropna().unique().tolist() 
        
        filter_dict[col] = st.sidebar.multiselect(
            f'Wähle {col} aus:',
            options=unique_values,
            default=unique_values
        )

    # --- Filter data ---
    df_filtered = df.copy()

    for col in selected_filters:
        selected_options = filter_dict[col]
        all_options = df[col].dropna().unique().tolist()
        
        if len(selected_options) < len(all_options):
            df_filtered = df_filtered[df_filtered[col].isin(selected_options)]

    # --- Show filtered data ---
    st.markdown(f"**Gefundene Einträge: {len(df_filtered)} von {len(df)}**")

    # Freeze columns by making them the index of the DataFrame
    display_df = df_filtered.copy()
    if frozen_cols:
        valid_frozen_cols = [c for c in frozen_cols if c in display_df.columns]
        if valid_frozen_cols:
            display_df = display_df.set_index(valid_frozen_cols)

    # Show and shine
    st.dataframe(display_df, use_container_width=True)

else:
    st.info("Bitte lade eine CSV-Datei hoch, um die Daten anzuzeigen.")
