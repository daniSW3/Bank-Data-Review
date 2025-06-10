





import pandas as pd
import oracledb
import os
import logging

# Set up logging
logging.basicConfig(filename='insert_data.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection parameters
username = "SYS"
password = "1234Dani@ethc#"
dsn = "AGPHOIT07.AGP.LOCAL:1521/xepdb1"
connection = None
cursor = None

try:
    # Connect to Oracle as SYSDBA
    logging.info("Attempting to connect to Oracle")
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn,
        mode=oracledb.SYSDBA
    )
    cursor = connection.cursor()
    print("Connected to Oracle")
    logging.info("Connected to Oracle")

    # Verify connection (optional)
    cursor.execute("SELECT * FROM v$version")
    for row in cursor:
        logging.info(f"Oracle Version: {row}")
    
    # Load data
    df = pd.read_csv(r"C:\Users\Daniel.Temesgen\Desktop\Bank-Data-Review\analysis_results.csv")
    logging.info(f"Loaded {len(df)} reviews from analysis_results.csv")

    # Insert banks into bank_reviews.banks
    banks = df["bank"].unique()
    bank_id_map = {}
    for bank_name in banks:
        try:
            cursor.execute(
                """
                INSERT INTO bank_reviews.banks (bank_name)
                VALUES (:1)
                """,
                [bank_name]
            )
            cursor.execute("SELECT bank_id FROM bank_reviews.banks WHERE bank_name = :1", [bank_name])
            bank_id_map[bank_name] = cursor.fetchone()[0]
        except oracledb.IntegrityError:
            cursor.execute("SELECT bank_id FROM bank_reviews.banks WHERE bank_name = :1", [bank_name])
            bank_id_map[bank_name] = cursor.fetchone()[0]

    # Insert reviews into bank_reviews.reviews
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO bank_reviews.reviews (
                review_id, bank_id, review_text, rating, review_date,
                sentiment_label, sentiment_score, themes, source
            )
            VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9)
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
    print(f"Inserted {len(df)} reviews into Oracle")
    logging.info(f"Inserted {len(df)} reviews into Oracle")

    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM bank_reviews.reviews")
    count = cursor.fetchone()[0]
    print(f"Total reviews in database: {count}")
    logging.info(f"Total reviews in database: {count}")

except oracledb.DatabaseError as e:
    error, = e.args
    print(f"Oracle Error: {error.code} - {error.message}")
    logging.error(f"Oracle Error: {error.code} - {error.message}")
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
    os.system('git add scripts/insert_data.py')
    os.system('git commit -m "Fix ORA-00942 by ensuring bank_reviews schema for Task 3"')
    os.system('git push origin task-3')