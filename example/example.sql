---------- [DDL]

DROP TABLE IF EXISTS `emps`;
DROP TABLE IF EXISTS `depts`;
CREATE TABLE `depts` (`deptno` int(11) NOT NULL, `name` varchar(128) DEFAULT NULL, PRIMARY KEY (`deptno`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `emps` (
`empno` int(11) NOT NULL DEFAULT '0',
  `name` varchar(128) DEFAULT NULL,
  `deptno` int(11) DEFAULT '0',
  `gender` varchar(128) DEFAULT NULL,
  `city` varchar(128) DEFAULT NULL,
  `empid` varchar(128) NOT NULL DEFAULT '0',
  `age` int(11) DEFAULT '0',
  `slacker` int(1) DEFAULT '0',
  `manager` int(1) DEFAULT '0',
  `joinedat` datetime DEFAULT NULL,
  PRIMARY KEY (`empno`,`empid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `depts` (`deptno`, `name`) VALUES
	(10,'Sales'),
	(20,'Marketing'),
	(30,'Accounts');

INSERT INTO `emps` (`empno`, `name`, `deptno`, `gender`, `city`, `empid`, `age`, `slacker`, `manager`, `joinedat`) VALUES
	(100,'Fred',10,NULL,NULL,'30',25,1,1,'1996-08-03 00:00:00'),
	(110,'John',40,'M','Vancouver','2',0,0,1,'2002-05-03 00:00:00'),
	(110,'Eric',20,'M','San Francisco','3',80,0,0,'2001-01-01 00:00:00'),
	(120,'Wilma',20,'F',NULL,'1',5,0,1,'2005-09-07 00:00:00'),
	(130,'Alice',40,'F','Vancouver','2',0,0,1,'2007-01-01 00:00:00');

---------- [Queries]

select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 1;
select d.deptno, max(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 1;
select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 0;
select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno;
