select * from products
order by UnitPrice desc;

select * from customers
 where Country in ('UK','Spain');

select * from products
 where UnitsInStock > 100 
   and UnitPrice >= 25;

select distinct customers.Country from orders join customers
    on orders.CustomerID = customers.CustomerID;

select * from orders
 where year(OrderDate) = 1996 
   and month(OrderDate) = 10;

select * from orders
 where ShipRegion is null 
   and ShipCountry = 'Germany'
   and Freight >= 100
   and EmployeeID = 1
   and year(Orderdate) = 1996;
   
select * from orders
 where ShippedDate > RequiredDate;

select * from orders
 where year(OrderDate) = 1997
   and month(OrderDate) <= 4
   and ShipCountry = 'Canada';

select * from orders
 where EmployeeID in (2,5,8)
   and ShipRegion is not null
   and ShipVia in (1,3)
order by EmployeeID, ShipVia;

select * from Employees
 where Region is null
   and year(BirthDate) <= 1960;