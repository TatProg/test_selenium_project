--Task 1
-- определить количество найденных и не найденных объектов
SELECT count(address_id)
FROM house_information
WHERE status is TRUE;

SELECT count(address)
FROM house_information
WHERE status is FALSE;

--Task 2
-- определить количество объектов для Материал несущих стен = Кирпичный по каждому региону
SELECT DISTINCT region, count(*) as Count
FROM house_information
WHERE house_information.walls_material LIKE 'Кирпич'
GROUP BY region;

--TASK 3
-- определить максимальное количество этажей для каждого Материал несущих стен в каждом городе
SELECT Distinct city, type_of_cellings, max(number_of_floors) as max_floors
FROM house_information
WHERE house_information.city is not null
  and house_information.type_of_cellings is not null
GROUP BY city, type_of_cellings;