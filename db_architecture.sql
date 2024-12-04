-- Création de la base de données
DROP DATABASE IF EXISTS perfumery;
CREATE DATABASE IF NOT EXISTS perfumery;
USE perfumery;

-- Table des clients
DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- Table des produits
DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    product_price DECIMAL(10, 2) NOT NULL
);

-- Table des gammes de produits
DROP TABLE IF EXISTS product_ranges;
CREATE TABLE IF NOT EXISTS product_ranges (
    range_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    range_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Table des références
DROP TABLE IF EXISTS range_references;
CREATE TABLE IF NOT EXISTS range_references (
    reference_id INT AUTO_INCREMENT PRIMARY KEY,
    range_id INT NOT NULL,
    reference_code VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (range_id) REFERENCES product_ranges(range_id)
);

DROP TABLE IF EXISTS salesperson;
CREATE TABLE salesperson (
    salesperson_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(15),
    region VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL,
    sales_target DECIMAL(10, 2)
);

-- Table des commandes
DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    salesperson_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (salesperson_id) REFERENCES salesperson(salesperson_id)
);

-- Table des détails des commandes
DROP TABLE IF EXISTS order_details;
CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    reference_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (reference_id) REFERENCES range_references(reference_id)
);



INSERT INTO salesperson (first_name, last_name, email, phone_number, region, hire_date, sales_target)
VALUES
    ('John', 'Doe', 'john.doe@example.com', '123-456-7890', 'North', '2022-01-15', 50000.00),
    ('Jane', 'Smith', 'jane.smith@example.com', '987-654-3210', 'South', '2023-03-22', 60000.00),
    ('Emily', 'Johnson', 'emily.johnson@example.com', '456-789-1230', 'East', '2021-07-10', 55000.00),
    ('Michael', 'Brown', 'michael.brown@example.com', '321-654-9870', 'West', '2020-11-05', 70000.00);




-- Insertion des clients français
INSERT INTO customers (first_name, last_name, email, phone_number, address, city, country)
VALUES
    ('Pierre', 'Martin', 'pierre.martin@example.com', '0601020304', '10 Rue de Paris', 'Paris', 'France'),
    ('Marie', 'Dupont', 'marie.dupont@example.com', '0612345678', '15 Avenue des Champs', 'Lyon', 'France'),
    ('Jacques', 'Durand', 'jacques.durand@example.com', '0623456789', '20 Boulevard Haussmann', 'Marseille', 'France');

-- Insertion des produits avec noms et prix
INSERT INTO products (product_name, product_price)
VALUES
    ('Eau de Parfum', 79.99),
    ('Eau de Toilette', 59.99),
    ('Bougie Parfumée', 29.99),
    ('Diffuseur de Parfum', 39.99);

-- Insertion des gammes
INSERT INTO product_ranges (product_id, range_name)
VALUES
    (1, 'Classique Collection'),
    (1, 'Luxe Collection'),
    (2, 'Sportive Collection'),
    (2, 'Voyage Collection');

-- Insertion des références
INSERT INTO range_references (range_id, reference_code)
VALUES
    (1, 'PAR-EDP-001'), (1, 'PAR-EDP-002'), (1, 'PAR-EDP-003'),
    (2, 'PAR-EDP-004'), (2, 'PAR-EDP-005'),
    (3, 'PAR-EDT-001'), (3, 'PAR-EDT-002'),
    (4, 'PAR-EDT-003'), (4, 'PAR-EDT-004');

-- Exemple de commande passée par un client
INSERT INTO orders (customer_id, salesperson_id, total_price)
VALUES
    (1, 1, 250.75),
    (2, 3, 1200.50),
    (3, 2, 489.99),
    (1, 4, 300.00);

-- Détails de la commande
INSERT INTO order_details (order_id, reference_id, quantity, price)
VALUES
    (1, 1, 1, 79.99), -- 1 Eau de Parfum (Classique Collection)
    (1, 3, 1, 59.99); -- 1 Eau de Toilette (Sportive Collection)


DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    role ENUM('admin', 'editor', 'viewer', 'customer') NOT NULL
);


INSERT INTO users (username, password, role)
VALUES
    ('admin', 'admin123', 'admin'),
    ('editor', 'editor123', 'editor'),
    ('viewer', 'viewer123', 'viewer'),
    ('customer','customer123','customer')
    ;
