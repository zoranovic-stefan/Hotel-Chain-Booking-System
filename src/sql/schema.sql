-- Create HotelChains table
CREATE TABLE IF NOT EXISTS HotelChains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    office_address VARCHAR(200) NOT NULL,
    num_hotels INTEGER DEFAULT 0
); -- done

CREATE TABLE IF NOT EXISTS HotelChainContact (
    id SERIAL PRIMARY KEY,
    hotel_chain_id INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    content VARCHAR(100) NOT NULL,
    CONSTRAINT fk_hotel_chain
        FOREIGN KEY (hotel_chain_id)
        REFERENCES HotelChains(id)
        ON DELETE CASCADE
); -- done


CREATE TABLE IF NOT EXISTS Hotels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    star_rating INT NOT NULL CHECK (star_rating BETWEEN 1 AND 5),
    hotel_chain_id INT NOT NULL,
    CONSTRAINT fk_hotel_chain
        FOREIGN KEY (hotel_chain_id)
        REFERENCES HotelChains(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS HotelContact (
    id SERIAL PRIMARY KEY,
    hotel_id INT NOT NULL,
    type VARCHAR(20) NOT NULL,
    content VARCHAR(100) NOT NULL,
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES Hotels(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS Rooms (
    id SERIAL PRIMARY KEY,
    room_number INT NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    is_extendable BOOLEAN NOT NULL,
    view_types VARCHAR(100),
    amenities VARCHAR(200) NOT NULL,
    problems VARCHAR(200),
    hotel_id INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES Hotels(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS Customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    registration_date DATE NOT NULL
); -- done

CREATE TABLE IF NOT EXISTS CustomerIdentification (
    id SERIAL PRIMARY KEY,
    id_type VARCHAR(50) NOT NULL,
    content VARCHAR(50) NOT NULL,
    customer_id INTEGER NOT NULL,
    driver_license VARCHAR(15) NOT NULL,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customers(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS EmployeeIdentification (
    id SERIAL PRIMARY KEY,
    id_type VARCHAR(50) NOT NULL,
    content VARCHAR(50) NOT NULL,
    employee_id INTEGER NOT NULL,
    CONSTRAINT fk_employee
        FOREIGN KEY (employee_id)
        REFERENCES Employees(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS Employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    hotel_id INT NOT NULL,
    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES Hotels(id)
        ON DELETE CASCADE
); -- done

CREATE TABLE IF NOT EXISTS Rentings (
    id SERIAL PRIMARY KEY,
    was_booked BOOLEAN NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    customer_id INT NOT NULL,
    room_id INT NOT NULL,
    employee_id INT NOT NULL,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customers(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_room
        FOREIGN KEY (room_id)
        REFERENCES Rooms(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_employee
        FOREIGN KEY (employee_id)
        REFERENCES Employees(id)
        ON DELETE CASCADE,
    CONSTRAINT invalid_date
        CHECK (check_in_date < check_out_date)
);--done

CREATE OR REPLACE FUNCTION inc_num_hotels()
   RETURNS TRIGGER AS $BODY$
    BEGIN
        UPDATE HotelChains
        SET num_hotels = num_hotels + 1
        WHERE id = NEW.hotel_chain_id;

        RETURN NEW;
    END;
$BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION dec_num_hotels()
   RETURNS TRIGGER AS $BODY$
    BEGIN
        UPDATE HotelChains
        SET num_hotels = num_hotels - 1
        WHERE id = OLD.hotel_chain_id;

        RETURN OLD;
    END;
$BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER inc_num_hotel
AFTER INSERT ON Hotels
FOR EACH ROW
EXECUTE FUNCTION inc_num_hotels();

CREATE OR REPLACE TRIGGER dec_num_hotel
AFTER DELETE ON Hotels
FOR EACH ROW
EXECUTE FUNCTION dec_num_hotels();



-- View 1: Available rooms per area
-- I'm using same hotel chain as the area
CREATE OR REPLACE VIEW available_rooms_per_chain AS
SELECT hc.name AS chain_name, COUNT(r.id) AS num_rooms FROM HotelChains hc
JOIN Hotels h ON hc.id = h.hotel_chain_id
JOIN Rooms r ON h.id = r.hotel_id
GROUP BY hc.id;

-- View 2: Aggregated capacity per hotel
CREATE OR REPLACE VIEW capacity_per_hotel AS
SELECT h.id AS hotel_id, h.name AS hotel_name, SUM(r.capacity) AS total_capacity
FROM Hotels h
JOIN Rooms r ON h.id = r.hotel_id
GROUP BY h.id;

-- indexes

-- this index is used a lot in aggregation
-- and rooms are commonly searched
CREATE INDEX IF NOT EXISTS rooms_capacity ON Rooms(capacity);

CREATE INDEX IF NOT EXISTS room_id ON Rooms(id);

CREATE INDEX IF NOT EXISTS hotel_id ON Hotels(id);