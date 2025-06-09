-- Creating sequence for bank_id
CREATE SEQUENCE banks_seq START WITH 1 INCREMENT BY 1;

-- Creating banks table
CREATE TABLE banks (
    bank_id NUMBER PRIMARY KEY,
    bank_name VARCHAR2(100) NOT NULL UNIQUE
);

-- Creating trigger for auto-incrementing bank_id
CREATE OR REPLACE TRIGGER banks_trigger
BEFORE INSERT ON banks
FOR EACH ROW
BEGIN
    SELECT banks_seq.NEXTVAL INTO :NEW.bank_id FROM dual;
END;
/

-- Creating reviews table
CREATE TABLE reviews (
    review_id NUMBER PRIMARY KEY,
    bank_id NUMBER NOT NULL,
    review_text CLOB NOT NULL,
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    review_date DATE,
    sentiment_label VARCHAR2(20),
    sentiment_score NUMBER CHECK (sentiment_score BETWEEN 0.0 AND 1.0),
    themes VARCHAR2(500),
    source VARCHAR2(50),
    CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
);

-- Committing changes
COMMIT;