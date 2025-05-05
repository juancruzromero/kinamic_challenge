import pandas as pd

def extract():
    """
    Extract data from a JSON file and load it into a DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing books data.
    """
    return pd.read_json('data/raw/books.json', encoding='utf-8')

def transform(df):
    """
    Clean the DataFrame by removing unnecessary characters and converting data types.
    
    Args:
        df (pd.DataFrame): DataFrame containing books clean data.
    """
    print("\nTransforming data...\n")
    # Clean prices data:
    df['price'] = df['price'].str.replace('£', '').astype(float)

    # Clean rating:
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3,
        'Four': 4, 'Five': 5
    }
    df['rating'] = df['rating'].map(rating_map)

    # Clean titles:
    df['title'] = df['title'].apply(lambda x: x.encode('latin1').decode('utf-8') if 'â' in x else x)
    
    return df

def load(df):
    """
    Save the cleaned DataFrame to a CSV file
    """
    df.to_csv('data/processed/books.csv', index=False, sep=";", encoding='utf-8')
    
def run_etl():
    """
    Run the ETL process: extract, transform, and load data.
    """
    print("\nStarting ETL process...")
    # Extract
    df = extract()
    # Transform
    df = transform(df)
    # Load
    load(df)
    print("ETL process completed successfully")