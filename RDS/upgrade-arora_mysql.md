# Upgrading from Aurora MySQL 1.x to 2.x

## Ref
1. https://aws.amazon.com/about-aws/whats-new/2021/01/amazon-aurora-supports-in-place-upgrades-mysql-5-6-to-5-7/
2. https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.MajorVersionUpgrade.html
3. https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.MajorVersionUpgrade.html#AuroraMySQL.Updates.MajorVersionUpgrade.1to2




upgrade to 1.22.3 as a first step


## The updated architecture includes the following steps:
### Pre-requiste
#### Aurora MySQL version 1 is compatible with MySQL 5.6. Aurora MySQL version 2 is compatible with MySQL 5.7. Aurora MySQL version 3 is compatible with MySQL 8.0
#### Enable binary logging on the blue environment

1. Perform fast database clone from the older Aurora major version (blue environment) and create it as an older Aurora major version (green environment).
## check database cluster version
```
aws rds describe-db-clusters --db-cluster-identifier test-cluster-green-old-cluster --query '*[].{EngineVersion:EngineVersion}' --output text
```
#### Note: If database cluster version is older than 1.22.3, a minor version upgrade take place.
2. Perform major version in-place upgrade by modifying the cluster on green environment.
3. Set up manual MySQL binary log replication between the Aurora clusters as shown in the architecture to replicate data changes from blue to green environments.
4. During the planned downtime window when the green environment is ready for switchover, stop the application blue environment and start using the green environment as new the blue environment.



















https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Updates.MajorVersionUpgrade.html#AuroraMySQL.Upgrading.GlobalDB
5.6.mysql_aurora.1.22.2
aws rds create-db-cluster --db-cluster-identifier raghib-cluster-identifier --engine aurora-mysql --db-cluster-version 5.7.mysql_aurora.2.11.0

aws rds describe-db-clusters --db-cluster-identifier test-cluster --query '*[].{EngineVersion:EngineVersion}' --output text

5.7.mysql_aurora.2.11.0

aws rds describe-db-engine-versions --engine aurora --engine-version 5.7.mysql_aurora.2.11.0 --query '*[].[ValidUpgradeTarget]'


### delete Arora mysql Cluster Identifier
```
aws rds describe-db-clusters --db-cluster-identifier test-db-identifier --output text --query '*[].["Cluster:",DBClusterIdentifier,DBClusterMembers[*].["Instance:",DBInstanceIdentifier,IsClusterWriter]]'

aws rds delete-db-cluster --db-cluster-identifier test-cluster-clone-cluster --skip-final-snapshot
``` 