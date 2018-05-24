select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 1;
select d.deptno, max(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 1;
select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno having count(*) > 0;
select d.deptno, min(e.empid) from test_db.emps as e join test_db.depts as d on e.deptno = d.deptno group by d.deptno;
