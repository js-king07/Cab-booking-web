CREATE DATABASE cab_booking;
USE cab_booking;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    phone VARCHAR(15) UNIQUE,
    otp VARCHAR(6)
);

CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15) UNIQUE,
    password VARCHAR(50),
    cab_type VARCHAR(20),
    latitude DOUBLE,
    longitude DOUBLE,
    status VARCHAR(20)
);

CREATE TABLE cabs (
    cab_id INT AUTO_INCREMENT PRIMARY KEY,
    cab_type VARCHAR(20),
    base_fare INT,
    per_km INT
);

INSERT INTO cabs (cab_type, base_fare, per_km) VALUES
('Bike', 20, 5),
('Auto', 30, 7),
('Mini', 50, 10),
('Prime SUV', 80, 15);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    driver_id INT,
    pickup VARCHAR(100),
    drop_location VARCHAR(100),
    cab_type VARCHAR(20),
    distance DOUBLE,
    fare DOUBLE,
    status VARCHAR(20)
);
