-- Count number of employees in each hotel
SELECT h.name AS hotel_name,
       COUNT(e.id) AS total_employees
FROM Hotels h
LEFT JOIN Employees e ON h.id = e.hotel_id
GROUP BY h.name
ORDER BY total_employees DESC;

-- Get hotel with most customers
SELECT h.name AS hotel_name,
       COUNT(DISTINCT r.customer_id) AS total_customers
FROM Hotels h
JOIN Rooms rm ON h.id = rm.hotel_id
JOIN Rentings r ON rm.id = r.room_id
GROUP BY h.id
HAVING COUNT(DISTINCT r.customer_id) = (
    SELECT MAX(customer_count)
    FROM (
        SELECT rm.hotel_id, COUNT(DISTINCT r.customer_id) AS customer_count
        FROM Rentings r
        JOIN Rooms rm ON r.room_id = rm.id
        GROUP BY rm.hotel_id
        ) AS customer_counts
    );

-- Get employees number of customers served
SELECT e.id AS employee_id, e.full_name AS full_name, COUNT(DISTINCT r.id) AS customers_served
FROM Employees e
JOIN Rentings r ON e.id = r.employee_id
GROUP BY e.id
ORDER BY customers_served DESC;

-- Get each hotel chain's average rating
SELECT hc.name AS hotel_chain,
       ROUND(AVG(h.star_rating), 2) AS avg_rating
FROM HotelChains hc
JOIN Hotels h ON hc.id = h.hotel_chain_id
GROUP BY hc.name
ORDER BY avg_rating DESC;