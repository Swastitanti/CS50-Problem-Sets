-- STEP 1: Crime scene report on Humphrey Street
SELECT *
FROM crime_scene_reports
WHERE year = 2024
    AND month = 7
    AND day = 28
    AND street = 'Humphrey Street';


-- STEP 2: Interviews conducted on July 28, 2024
SELECT *
FROM interviews
WHERE year = 2024
    AND month = 7
    AND day = 28;


-- STEP 3: ATM withdrawals at Leggett Street
SELECT *
FROM atm_transactions
WHERE year = 2024
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw';


-- STEP 4: People who made those withdrawals
SELECT DISTINCT people.name, people.phone_number
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2024
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = 'Leggett Street'
    AND atm_transactions.transaction_type = 'withdraw';


-- STEP 5: Earliest flight from Fiftyville on July 29
SELECT flights.id, flights.hour, flights.minute, airports.city
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
    AND flights.year = 2024
    AND flights.month = 7
    AND flights.day = 29
ORDER BY flights.hour, flights.minute
LIMIT 1;


-- STEP 6: Passengers on the earliest flight (ID 36 assumed)
SELECT people.name, people.phone_number
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
WHERE passengers.flight_id = 36;


-- STEP 7: Manually match names from ATM and flight to identify thief
-- STEP 8: Phone calls on July 28 under 60 seconds
SELECT caller, receiver
FROM phone_calls
WHERE year = 2024
    AND month = 7
    AND day = 28
    AND duration < 60;


-- STEP 9: Identify accomplice based on receiver (replace with correct number)
SELECT name
FROM people
WHERE phone_number = 'XXX-XXXX';
