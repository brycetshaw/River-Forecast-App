## Deploy a mysql database to a remote docker container

I deployed a mysql database to a cybera vm using a docker container. It wasn't very hard, these are the steps I followed:

1. Remove all other VMs.
2. Create a new VM from Ubuntu 18.04 image, size medium, add floating point ip address, and ssh key saved from before
3. Add security group rules to allow ingress and egress traffic on port 3306.
4. ssh into VM
5.  $sudo apt install docker.io
6. Follow this guide ALL THE WAY TO THE BOTTOM! https://medium.com/@backslash112/start-a-remote-mysql-server-with-docker-quickly-9fdff22d23fd
7. Enter the mysql console on the vm using commands given in (6). Look up your local ip address and add it to the credentials as explained here https://stackoverflow.com/questions/50177216/how-to-grant-all-privileges-to-root-user-in-mysql-8-0
8. Open one of our mysql database assignments and set the ip address in the jdbc connector to the floating point ip address of your vm, the username and passwords to what you just set in (7).
9. Your client manager project should now be attached to a mysql database, inside a docker container, inside a cybera vm. Good work. I think you will need to replicate the mysql user creation step every time you run this program from a new wifi network.

## Deploy React app + Nginx server to a remote docker container

https://medium.com/@tiangolo/react-in-docker-with-nginx-built-with-multi-stage-docker-builds-including-testing-8cc49d6ec305



## Restart Docker Container and then add users to database

docker ps -a

docker start river-app-front-end

docker exec -it mysql01 mysql -u root -p

!3N(eHezZoJdecYtoRc4rJamYnE

CREATE USER 'riverapp'@'172.219.147.63' IDENTIFIED BY 'riverapp';

GRANT ALL PRIVILEGES ON *.* TO 'riverapp'@'172.219.147.63' WITH GRANT OPTION;

```sql
docker ps -a
docker start river-app-front-end
docker exec -it mysql01 mysql -u root -p
!3N(eHezZoJdecYtoRc4rJamYnE

CREATE USER 'riverapp'@'172.103.187.218' IDENTIFIED BY 'riverapp';
GRANT ALL PRIVILEGES ON *.* TO 'riverapp'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```



## Some SQL queries for use in a dockerized mysql container

https://www.youtube.com/watch?v=HXV3zeQKqGY

Some commands I used (1:15:49 - 1:40:00 in the video):
Setting up a local mysql using docker:
docker pull mysql/mysql-server:latest
docker run --name=mysql1 -d mysql/mysql-server
docker ps -a
docker logs mysql1 2>&1 | grep GENERATED
docker exec -it mysql1 mysql -uroot -p

2. Adding a database, table, and rows:
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
CREATE DATABASE learnSQL;
USE learnSQL;
CREATE TABLE student(
    -> student_id INT PRIMARY KEY,
    -> name VARCHAR(20),
    -> major VARCHAR(20)
    -> );
OR...
CREATE TABLE student(
    -> student_id INT,
    -> name VARCHAR(20),
    -> major VARCHAR(20),
    -> PRIMARY KEY(student_id)
    -> );
DESCRIBE student;
ALTER TABLE student ADD gpa DECIMAL(3,2);
ALTER TABLE student DROP COLUMN gpa;
INSERT INTO student VALUES(1, 'Jack', 'Biology');
INSERT INTO student VALUES(2, 'Kate', 'Sociology');
INSERT INTO student(student_id,name) VALUES(3, 'Claire'); // Creates null value for major.
//duplicate primary keys is not allowed.
DROP TABLE student;