CREATE TABLE T3 (C0 INTEGER NULL, C1 BOOLEAN, C2 VARCHAR(13) NOT NULL);

SELECT ALL C2
FROM T3
WHERE 3 = 8;

SELECT C0
FROM T3
WHERE POWER(0, (3)) >= ABS((6));

SELECT *
FROM T3
WHERE ABS(T3.C0 / 7) < ABS(ABS(10));

