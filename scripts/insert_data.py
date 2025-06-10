import pandas as pd
import pyodbc
import os
import logging

# Set up logging
logging.basicConfig(filename='insert_data.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection parameters
server = r'AGPHOIT07\SQLEXPRESS'
database = 'bank_reviews'
connection = None
cursor = None

try:
    # Connect to SQL Server with Windows Authentication
    logging.info("Attempting to connect to SQL Server")
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    connection = pyodbc.connect(conn_str)
    cursor = connection.cursor()
    print("Connected to SQL Server")
    logging.info("Connected to SQL Server")

    # Load and validate data
    df = pd.read_csv(r"C:\Users\Daniel.Temesgen\Desktop\Bank-Data-Review\analysis_results.csv")
    logging.info(f"Loaded {len(df)} reviews from analysis_results.csv")
    required_columns = ['review_id', 'bank', 'review', 'rating', 'review_date', 'sentiment_label', 'sentiment_score', 'themes', 'source']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")
    
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating', 'review_id', 'sentiment_score'])
    df['rating'] = df['rating'].astype(int)
    df['review_id'] = df['review_id'].astype(int)

    # Insert banks
    banks = df["bank"].unique()
    bank_id_map = {}
    for bank_name in banks:
        try:
            cursor.execute(
                """
                INSERT INTO dbo.banks (bank_name)
                VALUES (?)
                """,
                (bank_name,)
            )
            cursor.execute("SELECT bank_id FROM dbo.banks WHERE bank_name = ?", (bank_name,))
            bank_id_map[bank_name] = cursor.fetchone()[0]
        except pyodbc.IntegrityError:
            cursor.execute("SELECT bank_id FROM dbo.banks WHERE bank_name = ?", (bank_name,))
            bank_id_map[bank_name] = cursor.fetchone()[0]

    # Insert reviews
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO dbo.reviews (
                review_id, bank_id, review_text, rating, review_date,
                sentiment_label, sentiment_score, themes, source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(row["review_id"]),
                bank_id_map[row["bank"]],
                str(row["review"]),
                int(row["rating"]),
                str(row["review_date"]),
                str(row["sentiment_label"]),
                float(row["sentiment_score"]),
                str(row["themes"]),
                str(row["source"])
            )
        )

    # Commit changes
    connection.commit()
    print(f"Inserted {len(df)} reviews into SQL Server")
    logging.info(f"Inserted {len(df)} reviews into SQL Server")

    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM dbo.reviews")
    count = cursor.fetchone()[0]
    print(f"Total reviews in database: {count}")
    logging.info(f"Total reviews in database: {count}")

except pyodbc.Error as e:
    print(f"SQL Server Error: {e}")
    logging.error(f"SQL Server Error: {e}")
except ValueError as e:
    print(f"Data Error: {e}")
    logging.error(f"Data Error: {e}")
except Exception as e:
    print(f"Error: {e}")
    logging.error(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# Commit to Git
if __name__ == "__main__":
    os.system('git add scripts/insert_data.py scripts/create_tables.sql')
    os.system('git commit -m "Add missing review_date and source columns for Task 3"')
    os.system('git push origin task-3')