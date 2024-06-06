use test;
CREATE TABLE R (X VARCHAR(10),Y VARCHAR(10));
CREATE TABLE S (Y VARCHAR(10),Z VARCHAR(10)); --创建表
insert into r values("X1","Y1");
insert into r values("X2","Y2");
insert into r values("X3","Y3");
insert into r values("X2","Y1");
insert into s values("Y1","Z1");
insert into s values("Y2","Z3"); --插入数据
--R÷S的过程
select distinct R1.X	-- 选择R里的X
from R R1
where not exists(	-- 不存在这个X对应的Y值
	select S.Y from S
	where not exists(	-- 这个Y值在S中没有对应的值
		select * from R R2
		where R2.Y=S.Y and R1.X=R2.X	-- 这句比较关键，把R和S联系起来
	)
);

-- 创建表
create table canteen(
    address varchar(32),
    canteen_name varchar(32),
    food_count int
);
create table food(
    food_name varchar(32),
    price int,
    taste varchar(32),
    canteen_name varchar(32)
);
-- 添加数据
insert into canteen values("韵苑","一食堂",0);
insert into canteen values("紫菘","二食堂",0);
insert into canteen values("喻园","三食堂",0);
insert into food values("盖浇饭",10,"辣","一食堂");
update canteen set food_count = food_count + 1 where canteen_name = "一食堂";
insert into food values("炒饭",10,"咸辣","二食堂");
update canteen set food_count = food_count + 1 where canteen_name = "二食堂";
insert into food values("面",10,"甜","二食堂");
update canteen set food_count = food_count + 1 where canteen_name = "二食堂";
insert into food values("盖浇饭",10,"咸","三食堂");
update canteen set food_count = food_count + 1 where canteen_name = "三食堂";
-- 查询全部的盖浇饭
select canteen.address,canteen.canteen_name,food.food_name,food.price,food.taste 
from canteen,food where food.food_name = "盖浇饭" and 
food.canteen_name = canteen.canteen_name;
-- 删除表中所有数据
truncate table canteen;
truncate table food;
-- 删除菜品
delete from food where food_name = "面" and canteen_name = "二食堂";
update canteen set food_count = food_count - 1 where canteen_name = "二食堂";
-- 删除食堂
delete from canteen where canteen_name = "二食堂";
delete from food where canteen_name = "二食堂";
-- 更改菜品
update food set food_name = food_name where food_name = "面" and canteen_name = "二食堂"; -- 更改菜品
update food set canteen_name = "一食堂" where food_name = "炒面" and canteen_name = "二食堂"; -- 更改食堂
update canteen set food_count = food_count + 1 where canteen_name = "一食堂";
update canteen set food_count = food_count - 1 where canteen_name = "二食堂";
-- 更改食堂
update canteen set address = "中操" where canteen_name = "二食堂" and address = "紫菘";
update canteen set canteen_name = "中操二食堂" where canteen_name = "二食堂" and address = "中操";
update food set canteen_name = "中操二食堂" where canteen_name = "二食堂";

