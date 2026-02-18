-- May add another file to this directory to DROP tables and dissolve the database if needed

-- intended for PostgreSQL
-- database is normalized in 3NF

-- items table is a new table to hold information about items
CREATE TABLE IF NOT EXISTS items (
    item_id VARCHAR(30) PRIMARY KEY,
    category VARCHAR(50),
    price FLOAT CHECK (price >= 0)
);

-- transactions table with the rest of the columns and some checks
-- all columns are dependent only on transaction_id
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY, -- unique identifier for each transaction (primary key)
    item_id VARCHAR(30) REFERENCES items(item_id) ON DELETE CASCADE,
    cust_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 1),
    total_spent FLOAT NOT NULL CHECK (total_spent >= 0),
    method VARCHAR(30) NOT NULL CHECK (
        method IN ('Digital Wallet', 'Credit Card', 'Cash')
    ),
    location VARCHAR(30) NOT NULL CHECK (
        location IN ('Online', 'In-Store')
    ),
    date DATE NOT NULL,
    has_discount BOOLEAN DEFAULT FALSE
);

--Rejected records table
-- it acts as "rejects" or error table, capturing bad or invalid
-- records instead of letting them fail silently
-- this table keeps track of bad data, saving the original record,
-- reason it failed, may add filepath later

CREATE TABLE IF NOT EXISTS rejected_records (
    reject_id SERIAL PRIMARY KEY, -- auto incrementing uniq id for each rejected record
    transaction_id VARCHAR(50),
    cust_id VARCHAR(50),
    category VARCHAR(50),
    item_id VARCHAR(50),
    price VARCHAR(50),
    quantity VARCHAR(50),
    total_spent VARCHAR(50),
    method VARCHAR(50),
    location VARCHAR(50),
    date VARCHAR(50),
    has_discount VARCHAR(50),
    error_info VARCHAR(80) NOT NULL
);

-- Indexes for performance
-- index helps the database find rows faster without scanning 
-- the entire table. 
CREATE INDEX IF NOT EXISTS idx_sales_customer
    ON transactions(cust_id);

CREATE INDEX IF NOT EXISTS idx_sales_date
    ON transactions(date);

CREATE INDEX IF NOT EXISTS idx_sales_item
    ON transactions(item_id);