# MYSQL_CONNECTOR SETUP INSTRUCTIONS
#----------------------------------------------------------------------------------------------------------
#
#  a. Install libaio first
#     dingze@wang:~$ cd ~
#     dingze@wang:~$ apt-cache search libaio
#     dingze@wang:~$ apt-get install libaio
#     dingze@wang:~$ sudo apt-get install libaio1
#
#  Note: In one of the steps below either b OR c, you'll be promted to enter root password. 
#        Please Enter that password carefull as this will be needed in future set of steps.
#
#  b. Download the MYSQL_CONNECTOR from web and follow all the instructions carefully
#     dingze@wang:~$ sudo dpkg -i Downloads/mysql-apt-config_0.8.10-1_all.deb
#     dingze@wang:~$ sudo apt-get update
#     
#  c. Next Step is to install MYSQL-SERVER
#     dingze@wang:~$ sudo apt-get install mysql-server
#
#  d. Now, add a group to the MYSQL Server
#     dingze@wang:~$ groupadd mysql
#
#  e. Now, we have to add an user which will access the MYSQL server
#     dingze@wang:~$ mysql -u root -p
#     Above will ask you to enter the root password. Please enter the Password created in Step 'b' OR 'c'
#
#  f. Now, we are under mysql command line, kindly enter below command to create a new user
#     mysql> CREATE USER 'pkuma1'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
#     mysql> GRANT ALL PRIVILEGES ON *.* TO 'pkuma1'@'localhost' WITH GRANT OPTION;
#
#     Note: In above you can pass any name instead of pkuma1 but rest remains the same. The second command
#           is necessary to grant all permissions to our created user.
#
#  Now, we are good with our MYSQL_CONNECTOR setup and we can execute below scripts safely in order:
#  a. sqlCreateScript.py
#  b. sqlInsertScript.py
#-----------------------------------------------------------------------------------------------------------
# 
#  Date Created: Apr 02, 2019
#  Created By  : Dingze Wang(dingzew)
#  Version     : 0.1(First)
#  Description : a. Creates database first with name: osdb_sql
#                b. Creates tables for master db
#                   1. USERS
#                   2. INDUSTRY
#                   3. CATEGORIES
#                   4. FACETS
#                   5. FACET_SEEDS
#                c. Creates tables for application db
#                   1. PROJECT
#                   2. PROJECT_HYPOTHESIS
#                   3. BRAND
#                   4. PROJECT_FACETS
#                   5. PROJECT_SEEDS
#                   6. FACET_VALUE
#                   7. FACET_VALUE_RESULTS
#                   8. PROJECT_STATUS
#-----------------------------------------------------------------------------------------------------------



from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'jacquard_sql'

#defining a list of tables that needs to be inserted in the database

#Master Table Creation Starts
TABLES = {}
TABLES['users'] = (
    "CREATE TABLE `users` ("
    "   `user_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `user_name` varchar(50) NOT NULL,"
    "   `user_password` char(64) NOT NULL,"
    "   `is_admin` enum('T','F') NOT NULL,"
    "   `user_status` enum('A','I') NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   PRIMARY KEY (`user_id`)"
    ") ENGINE=InnoDB")

TABLES['industry'] = (
    "CREATE TABLE `industry` ("
    "   `industry_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `industry_name` varchar(250) NOT NULL,"
    "   `industry_description` varchar(250) NOT NULL,"
    "   `naics_code` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`industry_id`),"
    "   CONSTRAINT `industry_ibfk_1` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['categories'] = (
    "CREATE TABLE `categories` ("
    "   `category_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `category_name` varchar(50) NOT NULL,"
    "   `category_description` varchar(250) NOT NULL,"
    "   `industry_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`category_id`),"
    "   CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`industry_id`) "
    "   REFERENCES `industry` (`industry_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `categories_ibfk_2` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['facets'] = (
    "CREATE TABLE `facets` ("
    "   `facet_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `facet_name` varchar(50) NOT NULL,"
    "   `facet_description` varchar(250) NOT NULL,"
    "   `category_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`facet_id`),"
    "   CONSTRAINT `facets_ibfk_1` FOREIGN KEY (`category_id`) "
    "   REFERENCES `categories` (`category_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `facets_ibfk_2` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")    

TABLES['facet_seeds'] = (
    "CREATE TABLE `facet_seeds` ("
    "   `seeds_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `seeds_name` varchar(50) NOT NULL,"
    "   `seeds_description` varchar(250) NOT NULL,"
    "   `facet_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`seeds_id`),"
    "   CONSTRAINT `facet_seeds_ibfk_1` FOREIGN KEY (`facet_id`) "
    "   REFERENCES `facets` (`facet_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `facet_seeds_ibfk_2` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

#Master Table Creation Ends

#Application Table Creation Starts
TABLES_APP = {}
TABLES_APP['project'] = (
    "CREATE TABLE `project` ("
    "   `project_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `project_name` varchar(50) NOT NULL,"
    "   `project_description` varchar(250) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `industry_id` int(11) NOT NULL,"
    "   `category_id` int(11) NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`project_id`),"
    "   CONSTRAINT `project_ibfk_1` FOREIGN KEY (`industry_id`) "
    "   REFERENCES `industry` (`industry_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_ibfk_2` FOREIGN KEY (`category_id`) "
    "   REFERENCES `categories` (`category_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_ibfk_3` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['project_hypothesis'] = (
    "CREATE TABLE `project_hypothesis` ("
    "   `hypothesis_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `hypothesis_name` varchar(50) NOT NULL,"
    "   `project_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`hypothesis_id`),"
    "   CONSTRAINT `project_hypothesis_ibfk_1` FOREIGN KEY (`project_id`) "
    "   REFERENCES `project` (`project_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_hypothesis_ibfk_2` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['brands'] = (
    "CREATE TABLE `brands` ("
    "   `brand_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `brand_name` varchar(50) NOT NULL,"
    "   `project_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `category_id` int(11) NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`brand_id`),"
    "   CONSTRAINT `brands_ibfk_1` FOREIGN KEY (`project_id`) "
    "   REFERENCES `project` (`project_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `brands_ibfk_2` FOREIGN KEY (`category_id`) "
    "   REFERENCES `categories` (`category_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `brands_ibfk_3` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['project_facets'] = (
    "CREATE TABLE `project_facets` ("
    "   `facet_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `facet_name` varchar(50) NOT NULL,"
    "   `project_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `category_id` int(11) NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`facet_id`),"
    "   CONSTRAINT `project_facets_ibfk_1` FOREIGN KEY (`project_id`) "
    "   REFERENCES `project` (`project_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_facets_ibfk_2` FOREIGN KEY (`category_id`) "
    "   REFERENCES `categories` (`category_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_facets_ibfk_3` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")    

TABLES_APP['project_seeds'] = (
    "CREATE TABLE `project_seeds` ("
    "   `seeds_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `seeds_name` varchar(50) NOT NULL,"
    "   `facet_id` int(11) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `user_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`seeds_id`),"
    "   CONSTRAINT `project_seeds_ibfk_1` FOREIGN KEY (`facet_id`) "
    "   REFERENCES `project_facets` (`facet_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `project_seeds_ibfk_2` FOREIGN KEY (`user_id`) "
    "   REFERENCES `users` (`user_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['facet_value'] = (
    "CREATE TABLE `facet_value` ("
    "   `facet_value_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `project_id` int(11) NOT NULL,"
    "   `seeds_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`facet_value_id`),"
    "   CONSTRAINT `facet_value_ibfk_1` FOREIGN KEY (`project_id`) "
    "   REFERENCES `project` (`project_id`) ON DELETE CASCADE,"
    "   CONSTRAINT `facet_value_ibfk_2` FOREIGN KEY (`seeds_id`) "
    "   REFERENCES `project_seeds` (`seeds_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['facet_value_results'] = (
    "CREATE TABLE `facet_value_results` ("
    "   `result_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `result_values` varchar(50) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `facet_value_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`result_id`),"
    "   CONSTRAINT `facet_value_results_ibfk_1` FOREIGN KEY (`facet_value_id`) "
    "   REFERENCES `facet_value` (`facet_value_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES_APP['project_status'] = (
    "CREATE TABLE `project_status` ("
    "   `status_id` int(11) NOT NULL AUTO_INCREMENT,"
    "   `status_value` varchar(50) NOT NULL,"
    "   `create_date` datetime NOT NULL,"
    "   `update_date` datetime NOT NULL,"
    "   `project_id` int(11) NOT NULL,"
    "   PRIMARY KEY (`status_id`),"
    "   CONSTRAINT `project_status_ibfk_1` FOREIGN KEY (`project_id`) "
    "   REFERENCES `project` (`project_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")
#Application Table Creation Ends

#connecting the database starts
#Change the Username/Password as per the user created
cnx = mysql.connector.connect(user='pkuma1', password='password', auth_plugin='mysql_native_password')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

print("Master Table Creation Starts")
for name, ddl in TABLES.items():
    try:
        print("Creating table {}:".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists")
        else:
            print(err.msg)
    else:
        print("OK")

print("Application Table Creation Starts")
for name, ddl in TABLES_APP.items():
    try:
        print("Creating table {}:".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists")
        else:
            print(err.msg)
    else:
        print("OK")

#Closing the Database connection
cursor.close()
cnx.close()
