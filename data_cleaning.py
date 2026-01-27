import pandas as pd
import numpy as np
from pathlib import Path


def load_and_clean_data(file_path=None, df=None, festivals_path=None):
    """
    Enhanced data cleaning function that can accept either file path or DataFrame
    
    Parameters:
    -----------
    file_path : str, optional
        Path to CSV file containing Date and Amount columns
    df : pd.DataFrame, optional
        DataFrame with Date and Amount columns (alternative to file_path)
    festivals_path : str, optional
        Path to festivals CSV file. If None, uses default location.
    
    Returns:
    --------
    pd.DataFrame : Cleaned data with all features
    """
    
    # Load data
    if df is not None:
        data_df = df.copy()
    elif file_path is not None:
        data_df = pd.read_csv(file_path)
    else:
        raise ValueError("Either file_path or df must be provided")
    
    # Ensure required columns exist
    if 'Date' not in data_df.columns or 'Amount' not in data_df.columns:
        raise ValueError("DataFrame must contain 'Date' and 'Amount' columns")
    
    # Keep only relevant columns
    df = data_df[['Date', 'Amount']].copy()
    # Convert to datetime using the correct format
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d", errors='coerce')

    # Check if conversion worked
    print("âœ… Parsed Dates:")
    print(df.head())

    # Convert Amount to numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # Drop nulls and negatives
    df = df.dropna(subset=['Date', 'Amount'])
    df = df[df['Amount'] >= 0]
    
    # Sort by true datetime
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Group by actual dates (day-level)
    df = df.groupby(df['Date'].dt.date).agg({'Amount': 'sum'}).reset_index()
    print(df.head())
    # Check result
    print(f"Loaded {len(df)} records")
    
    # Create continuous full date range
    df['Date'] = pd.to_datetime(df['Date'])
    full_dates = pd.DataFrame({
        'Date': pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
    })
    
    # Merge with main data
    merged_df = pd.merge(full_dates, df, on='Date', how='left')
    
    # Create Holiday_flag (1 if missing, else 0)
    merged_df['Holiday_flag'] = merged_df['Amount'].isna().astype(int)
    
    # Fill missing Amounts with 0
    merged_df['Amount'] = merged_df['Amount'].fillna(0)
    
    print(f"âœ… Total holidays detected: {merged_df['Holiday_flag'].sum()}")
    
    # Add weekend_flag
    merged_df['DayOfWeek'] = merged_df['Date'].dt.dayofweek
    merged_df['Weekend_flag'] = merged_df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    merged_df = merged_df.drop(columns=['DayOfWeek'])
    print(f"âœ… Total weekends detected: {merged_df['Weekend_flag'].sum()}")
    
    # Load and merge festivals
    if festivals_path is None:
        # Try default locations
        possible_paths = [
            Path('Festivals.csv'),
            Path('../Festivals.csv'),
            Path('data/Festivals.csv'),
        ]
        
        for path in possible_paths:
            if path.exists():
                festivals_path = str(path)
                break
    
    if festivals_path and Path(festivals_path).exists():
        festivals = pd.read_csv(festivals_path)
        festivals['Date'] = pd.to_datetime(festivals['Date'], errors='coerce')
        
        # Group festivals by date and join names with comma
        festival_grouped = festivals.groupby('Date')['Festival_Name'].apply(
            lambda x: ','.join(x)
        ).reset_index()
        
        # Merge with main data
        data = merged_df.merge(festival_grouped, on='Date', how='left')
        
        # Add Festival_flag: 1 if festival exists, else 0
        data['Festival_flag'] = data['Festival_Name'].notna().astype(int)
        
        # Fill NaN Festival_Name with empty string
        data['Festival_Name'] = data['Festival_Name'].fillna('')
        print(f"âœ… Total festivals detected: {data['Festival_flag'].sum()}")
    else:
        print("âš ï¸  No festivals file found, proceeding without festival data")
        data = merged_df.copy()
        data['Festival_flag'] = 0
        data['Festival_Name'] = ''
    
    cleaned_data = data[['Date', 'Amount', 'Holiday_flag', 'Weekend_flag', 'Festival_flag', 'Festival_Name']]
    
    return cleaned_data


def aggregate_multi_branch_data(df, group_by_cols=['Date'], agg_col='Amount'):
    """
    Aggregate multi-branch/zone data by date
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with Date, Amount, and optionally Branch/Zone columns
    group_by_cols : list
        Columns to group by (default: ['Date'])
    agg_col : str
        Column to aggregate (default: 'Amount')
    
    Returns:
    --------
    pd.DataFrame : Aggregated data
    """
    
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Group and aggregate
    agg_df = df.groupby(group_by_cols).agg({agg_col: 'sum'}).reset_index()
    
    return agg_df


# Backward compatibility with original function signature
def load_and_clean_data_legacy(file_path):
    """Legacy function for backward compatibility"""
    return load_and_clean_data(file_path=file_path)