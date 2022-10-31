Ref https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateVPC.html

1. Create a VPC with private and public subnets

2. Create a VPC security group for a public web server

3. Create a VPC security group for a private DB instance

4. Create a DB subnet group
    - Note the subnet IDs of the subnets named tutorial-subnet-private1-us-west-2a and tutorial-subnet-private2-us-west-2b.
    
    Test-subnet-private1-ap-south-1a    subnet-042c6d4fbb5726cdb
    Test-subnet-private2-ap-south-1b    subnet-0744a46aeb0ded2a0

    You need the subnet IDs when you create your DB subnet group.

****************************************************************
# Create a DB Instance

# Ref https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html

****************************************************************
# Install a web server

# Ref: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateWebServer.html
## Install a web server on your EC2 instance
```
sudo yum update -y
sudo amazon-linux-extras install -y php8.0 mariadb10.5
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
```
    
### To set file permissions for the Apache web server

1. Add the ec2-user user to the apache group.
```
sudo usermod -a -G apache ec2-user
```
2. Log out to refresh your permissions and include the new apache group.
```
exit
```
3. Log back in again and verify that the apache group exists with the groups command.
```
groups
```     
4. Change the group ownership of the /var/www directory and its contents to the apache group.
```
sudo chown -R ec2-user:apache /var/www
```    
5. Change the directory permissions of /var/www and its subdirectories to add group write permissions and set the group ID on subdirectories created in the future.
```
sudo chmod 2775 /var/www
find /var/www -type d -exec sudo chmod 2775 {} \;
```    
6. Recursively change the permissions for files in the /var/www directory and its subdirectories to add group write permissions.
```
find /var/www -type f -exec sudo chmod 0664 {} \;
```

## Connect your Apache web server to your DB instance

1. While still connected to your EC2 instance, change the directory to /var/www and create a new subdirectory named inc.
```
cd /var/www
mkdir inc
cd inc
```
2. Create a new file in the inc directory named dbinfo.inc, and then edit the file by calling nano (or the editor of your choice).
```
vi dbinfo.inc
```
3. Add the following contents to the dbinfo.inc file. Here, db_instance_endpoint is your DB instance endpoint, without the port, and master password is the master password for your DB instance.

### Note: We recommend placing the user name and password information in a folder that isn't part of the document root for your web server. Doing this reduces the possibility of your security information being exposed.
```
<?php

define('DB_SERVER', 'db_instance_endpoint');
define('DB_USERNAME', 'tutorial_user');
define('DB_PASSWORD', 'master password');
define('DB_DATABASE', 'sample');

?>
```              
4. Change the directory to /var/www/html.
```
cd /var/www/html
```
5. Create a new file in the html directory named SamplePage.php, and then edit the file by calling nano (or the editor of your choice).
```
vi SamplePage.php
```                
6. Add the following contents to the SamplePage.php file:
```
<?php include "../inc/dbinfo.inc"; ?>
<html>
<body>
<h1>Sample page</h1>
<?php

  /* Connect to MySQL and select the database. */
  $connection = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD);

  if (mysqli_connect_errno()) echo "Failed to connect to MySQL: " . mysqli_connect_error();

  $database = mysqli_select_db($connection, DB_DATABASE);

  /* Ensure that the EMPLOYEES table exists. */
  VerifyEmployeesTable($connection, DB_DATABASE);

  /* If input fields are populated, add a row to the EMPLOYEES table. */
  $employee_name = htmlentities($_POST['NAME']);
  $employee_address = htmlentities($_POST['ADDRESS']);

  if (strlen($employee_name) || strlen($employee_address)) {
    AddEmployee($connection, $employee_name, $employee_address);
  }
?>

<!-- Input form -->
<form action="<?PHP echo $_SERVER['SCRIPT_NAME'] ?>" method="POST">
  <table border="0">
    <tr>
      <td>NAME</td>
      <td>ADDRESS</td>
    </tr>
    <tr>
      <td>
        <input type="text" name="NAME" maxlength="45" size="30" />
      </td>
      <td>
        <input type="text" name="ADDRESS" maxlength="90" size="60" />
      </td>
      <td>
        <input type="submit" value="Add Data" />
      </td>
    </tr>
  </table>
</form>

<!-- Display table data. -->
<table border="1" cellpadding="2" cellspacing="2">
  <tr>
    <td>ID</td>
    <td>NAME</td>
    <td>ADDRESS</td>
  </tr>

<?php

$result = mysqli_query($connection, "SELECT * FROM EMPLOYEES");

while($query_data = mysqli_fetch_row($result)) {
  echo "<tr>";
  echo "<td>",$query_data[0], "</td>",
       "<td>",$query_data[1], "</td>",
       "<td>",$query_data[2], "</td>";
  echo "</tr>";
}
?>

</table>

<!-- Clean up. -->
<?php

  mysqli_free_result($result);
  mysqli_close($connection);

?>

</body>
</html>


<?php

/* Add an employee to the table. */
function AddEmployee($connection, $name, $address) {
   $n = mysqli_real_escape_string($connection, $name);
   $a = mysqli_real_escape_string($connection, $address);

   $query = "INSERT INTO EMPLOYEES (NAME, ADDRESS) VALUES ('$n', '$a');";

   if(!mysqli_query($connection, $query)) echo("<p>Error adding employee data.</p>");
}

/* Check whether the table exists and, if not, create it. */
function VerifyEmployeesTable($connection, $dbName) {
  if(!TableExists("EMPLOYEES", $connection, $dbName))
  {
     $query = "CREATE TABLE EMPLOYEES (
         ID int(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
         NAME VARCHAR(45),
         ADDRESS VARCHAR(90)
       )";

     if(!mysqli_query($connection, $query)) echo("<p>Error creating table.</p>");
  }
}

/* Check for the existence of a table. */
function TableExists($tableName, $connection, $dbName) {
  $t = mysqli_real_escape_string($connection, $tableName);
  $d = mysqli_real_escape_string($connection, $dbName);

  $checktable = mysqli_query($connection,
      "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME = '$t' AND TABLE_SCHEMA = '$d'");

  if(mysqli_num_rows($checktable) > 0) return true;

  return false;
}
?>                        
```
7. Verify that your web server successfully connects to your DB instance by opening a web browser and browsing to http://EC2 instance endpoint/SamplePage.php, for example: http://ec2-55-122-41-31.us-west-2.compute.amazonaws.com/SamplePage.ph

## Connecting to a DB instance running the MySQL database engine
yum install mariadb
mysql -h databse-1-cluster.cluster-cygdv6gy86fw.ap-south-1.rds.amazonaws.com -P 3306 -u admin -p

