SELECT *
FROM   read_json('data/simple/employees.json');

SELECT department,
       avg(salary)
FROM   read_json('data/simple/employees.json')
GROUP  BY all;
