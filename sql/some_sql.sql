-- May contain the SQL statements for CREATING the tables to initialize the database
-- May add another file to this directory to DROP tables and dissolve the database if needed
-- how many tables, normalize it

-- staging table for valid data
-- this table stores validated sales transaction records
-- with built-in rules to maintain clean and structured data

-- it defines the structure and rules for storing individual sales transactions,
-- including validation constraints to ensure clean and consistent data.

CREATE TABLE stg_sales (
    transaction_id TEXT PRIMARY KEY, -- unique identifier for each transaction (primary key)
    customer_id TEXT NOT NULL,
    category TEXT NOT NULL, 
    item TEXT NOT NULL,
    price_per_unit NOT NULL CHECK (price_per_unit >= 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 1),
    total_spent NOT NULL CHECK (total_spent >= 0),
    payment_method TEXT NOT NULL CHECK (
        payment_method IN ('Digital Wallet', 'Credit Card', 'Cash')
    ),
    location TEXT NOT NULL CHECK (
        location IN ('Online', 'In-Store')
    ),
    transaction_date DATE NOT NULL,
    discount_applied BOOLEAN DEFAULT FALSE,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Rejected records table
-- it acts as "rejects" or error table, capturing bad or invalid
-- records instead of letting them fail silently
-- this table keeps track of bad data, saving the original record,
-- reason it failed, when it failed. 

CREATE TABLE stg_rejects (
    reject_id SERIAL PRIMARY KEY, -- auto incrementing uniq id for each rejected record
    raw_record JSONB NOT NULL,
    error_info TEXT NOT NULL,
    source_type TEXT CHECK (source_type IN ('CSV', 'JSON')),
    rejected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
-- index helps the database find rows faster without scanning 
--the entire table. 
CREATE INDEX idx_sales_customer. 
    ON stg_sales(customer_id);

CREATE INDEX idx_sales_date
    ON stg_sales(transaction_date);

CREATE INDEX idx_sales_category
    ON stg_sales(category);

CREATE INDEX idx_sales_item
    ON stg_sales(item);

-- indexes improves filtering speed
-- makes your stg_sales faster to search by:
-- customer, date, category, item