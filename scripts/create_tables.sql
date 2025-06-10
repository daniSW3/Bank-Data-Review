CREATE SEQUENCE bank_reviews.banks_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE bank_reviews.banks (
    bank_id NUMBER PRIMARY KEY,
    bank_name VARCHAR2(100) UNIQUE
);

CREATE TABLE bank_reviews.reviews (
    review_id NUMBER PRIMARY KEY,
    bank_id NUMBER,
    review_text VARCHAR2(4000),
    rating NUMBER,
    review_date DATE,
    sentiment_label VARCHAR2(50),
    sentiment_score NUMBER,
    themes VARCHAR2(4000),
    source VARCHAR2(100),
    CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES bank_reviews.banks(bank_id)
);

CREATE OR REPLACE TRIGGER bank_reviews.bi_banks
    BEFORE INSERT ON bank_reviews.banks
    FOR EACH ROW
BEGIN
    SELECT banks_seq.NEXTVAL INTO :NEW.bank_id FROM dual;
END;
/