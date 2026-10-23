CREATE TABLE t as SELECT * FROM read_json('data/simple/employees.json')

SELECT * EXCLUDE salary FROM t

FROM t
SELECT * EXCLUDE salary 
WHERE age < 30

SELECT department, avg_salary: avg(salary) 
FROM t 
GROUP  BY all 
HAVING avg_salary > 50000


