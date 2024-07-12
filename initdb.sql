CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE staff_user (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    department_id INTEGER REFERENCES departments(id),
    password VARCHAR(255)
);

CREATE TABLE epic_user (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(255),
    company VARCHAR(255),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    assign_to INTEGER REFERENCES staff_user(staff_id)
);

CREATE TABLE epic_contract (
    contract_id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES epic_user(user_id),
    total_amount NUMERIC,
    amount_due NUMERIC,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status status_contract,
    commercial_contact INTEGER REFERENCES staff_user(staff_id)
);

CREATE TYPE status_contract AS ENUM ('To sign', 'Signed', 'Cancelled');

CREATE TABLE epic_event (
    id SERIAL PRIMARY KEY,
    contract INTEGER REFERENCES epic_contract(contract_id),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    support_contact INTEGER REFERENCES staff_user(staff_id),
    location VARCHAR(255),
    attendees INTEGER,
    notes TEXT
);