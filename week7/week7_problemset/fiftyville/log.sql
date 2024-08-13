-- Keep a log of any SQL queries you execute as you solve the mystery.

--see the crime_sceen_report
SELECT * FROM crime_scene_reports WHERE street = 'Humphrey Street' AND month = '7' AND day = '28' AND year = '2023';
-- report id is 295, time of theft is 10:15am at the bakery, three witnesses


--find the interviews with the witnesses
SELECT * FROM interviews WHERE year = '2023' AND month = '7' AND day = '28';
--Ruth interveiw_id-161- ' Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.'

--Eugene interveiw_id-162- 'I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I
--arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.'

--Raymond interveiw_id-163- 'As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
--In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--The thief then asked the person on the other end of the phone to purchase the flight ticket.'


--check bakery cams in the timeframe given by Ruth
SELECT * FROM bakery_security_logs WHERE year = '2023' AND month = '7' AND day = '28' AND hour = '10' AND minute >= '15' AND minute <= '25';
--thief has one of these license_plates: 5P2BI95  94KL13X  6P58WS2  4328GD8  G412CB7  L93JTIZ  322W7JE  0NTHK55


--Find phone calls no the correct date that are less than a minute
SELECT * FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND  duration < 60;
--caller: (130) 555-0289 r: (996) 555-8899
--caller: (499) 555-9472 r: (892) 555-8872
--caller: (367) 555-5533 r: (375) 555-8161
--caller: (499) 555-9472 r: (717) 555-1342
--caller: (286) 555-6063 r: (676) 555-6554
--caller: (770) 555-1861 r: (725) 555-3243
--caller: (031) 555-6622 r: (910) 555-3251
--caller: (826) 555-1652 r: (066) 555-9701
--caller: (338) 555-6650 r: (704) 555-2131


--find the people who made a <60sec call from the bakery that day.
SELECT * FROM people WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55') AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND  duration < 60);
--    id   |  name  |  phone_number  | passport_number | license_plate |
--| 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
--| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |


--narrow down suspects based on phone calls made by those leaving the bakery and the atm transaction
--SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
SELECT * FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55') AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND  duration < 60) AND bank_accounts. account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw');
--Bruce -account_number: 49610011
--Diana -account_number: 26013199


--find the possible accomplice of suspect Bruce
SELECT * FROM people WHERE phone_number = '(375) 555-8161';
--|   id   | name  |  phone_number  | passport_number | license_plate |
--| 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |


--find the possible accomplice of suspect Diana
SELECT * FROM people WHERE phone_number = '(725) 555-3243';
--|   id   |  name  |  phone_number  | passport_number | license_plate |
--| 847116 | Philip | (725) 555-3243 | 3391710505      | GW362R6       |


--find fiftyville airport
SELECT * FROM airports WHERE city = 'Fiftyville';
--| id | abbreviation |          full_name          |    city    |
--| 8  | CSF          | Fiftyville Regional Airport | Fiftyville |


--find earlist flight from fiftyville on the 29th
SELECT * FROM flights WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = 8;
--| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
--| 36 | 8                 | 4                      | 2023 | 7     | 29  | 8    | 20     |


--find the city the thief escaped to
SELECT * FROM airports WHERE id = 4;
--city is New York


--find the passenger list of the flight the thief took
SELECT * FROM passengers WHERE flight_id = 36;
--Bruce is the thief and Robin is the accomplice
