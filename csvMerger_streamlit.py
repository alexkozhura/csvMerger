import os, pandas as pd
import streamlit as st

def process_files_test(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Determine which is df1 and df2
    if len(df1.columns) == 1:
        df_single_column = df1.copy()
        df_multi_column = df2.copy()
    else:
        df_single_column = df2.copy()
        df_multi_column = df1.copy()
    
    # Rename the first column to 'Creative (UA)' in both DataFrames
    df_single_column.columns = ['Creative (UA)']
    df_multi_column.columns.values[0] = 'Creative (UA)'
    
    # Determine columns to keep
    if 'Installs' in df_multi_column.columns:
        cols_to_keep = ['Creative (UA)', 'Impressions', 'Installs', 'IPM']
        df_multi_column.replace('-', 0, inplace=True)
    elif 'installs' in df_multi_column.columns:
        cols_to_keep = ['Creative (UA)', 'impressions', 'installs', 'ipm']
    else:
        cols_to_keep = df_multi_column.columns.tolist()  # or handle the error
        
    df_multi_column = df_multi_column[cols_to_keep]
    
    # Merge the DataFrames
    merged_df = pd.merge(df_single_column, df_multi_column, on='Creative (UA)', how='left').fillna(0)

    # Explicitly convert 'impressions' and 'installs' to integers after merge
    for col in ['Impressions', 'impressions', 'Installs', 'installs']:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].astype(float).astype(int).replace(0, '')

    # Format other columns to 1 decimal place
    for col in merged_df.columns:
        if col not in ['Impressions', 'impressions', 'Installs', 'installs', 'Creative (UA)']:
            merged_df[col] = merged_df[col].astype(float).round(1).replace(0.0, '')

    return merged_df

def process_files_ongoing(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Determine which is df1 and df2
    if len(df1.columns) == 1:
        df_single_column = df1.copy()
        df_multi_column = df2.copy()
    else:
        df_single_column = df2.copy()
        df_multi_column = df1.copy()
    
    # Rename the first column to 'Creative (UA)' in both DataFrames
    df_single_column.columns = ['Creative (UA)']
    df_multi_column.columns.values[0] = 'Creative (UA)'
    
    # Determine columns to keep
    if 'Installs' in df_multi_column.columns:
        cols_to_keep = ['Creative (UA)', 'Installs', 'Spend', 'IPM', 'RR D7 To-Date', 'eARPU D365 Forecast', 'eROAS D365 Forecast']
        df_multi_column.replace('-', 0, inplace=True)
    elif 'installs' in df_multi_column.columns:
        cols_to_keep = ['Creative (UA)', 'installs', 'revenue', 'ipm']
        df_multi_column['revenue'] = df_multi_column['revenue'].str.replace('$', '').astype(float)
    else:
        cols_to_keep = df_multi_column.columns.tolist()  # or handle the error
        
    df_multi_column = df_multi_column[cols_to_keep]
    
    # Merge the DataFrames
    merged_df = pd.merge(df_single_column, df_multi_column, on='Creative (UA)', how='left').fillna(0)

    # Explicitly convert 'impressions' and 'installs' to integers after merge
    for col in ['Impressions', 'impressions', 'Installs', 'installs']:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].astype(float).astype(int).replace(0, '')

    # Format other columns to 1 decimal place
    for col in merged_df.columns:
        if col not in ['Impressions', 'impressions', 'Installs', 'installs', 'Creative (UA)']:
            merged_df[col] = merged_df[col].astype(float).round(1).replace(0.0, '')

    return merged_df

def main():
    st.title("CSV Merge Tool 1.0")

    mode = st.radio("Choose mode:", ('Test', 'Ongoing'))

    file1 = st.file_uploader("Upload CSV File 1 (список креативов, колонка может называться Creative)", type="csv")
    file2 = st.file_uploader("Upload CSV File 2 (выгрузка из Appodeal BI или Appgrowth BI)", type="csv")

    if file1 and file2:
        if mode == "Test":
            merged_df = process_files_test(file1, file2)

        elif mode == "Ongoing":
            merged_df = process_files_ongoing(file1, file2)
        
        # Display the merged files 
        st.write("Merged Files:")
        st.write(merged_df)

        st.download_button(
            label="Download CSV",
            data=merged_df.to_csv(index=False),
            file_name="merged_files.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()