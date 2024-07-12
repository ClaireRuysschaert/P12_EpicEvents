CREATE DATABASE epic_events_db;
\c epic_events_db;

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

INSERT INTO departments (name) VALUES ('Management'), ('Support'), ('Commercial');

INSERT INTO staff_user (first_name, last_name, email, department_id, password) VALUES
('John', 'Doe', 'john.doe@example.com', 2, 'password123'),
('Jane', 'Smith', 'jane.smith@example.com', 3, 'password456');

INSERT INTO epic_user (first_name, last_name, email, phone, company, assign_to) VALUES
('Alice', 'Johnson', 'alice.johnson@example.com', '0666666666', 'Company A', 2),
('Bob', 'Brown', 'bob.brown@example.com', '0777777777', 'Company B', 2);

INSERT INTO epic_contract (client_id, total_amount, amount_due, status, commercial_contact) VALUES
(1, 1000.00, 500.00, 'To sign', 2),
(2, 2000.00, 1500.00, 'Signed', 2);

INSERT INTO epic_event (contract, start_date, end_date, support_contact, location, attendees, notes) VALUES
(1, '2023-10-01 10:00:00', '2024-10-01 12:00:00', 2, 'Location A', 50, 'Event notes for contract 1'),
(2, '2023-11-01 14:00:00', '2024-11-01 16:00:00', 2, 'Location B', 100, 'Event notes for contract 2');
