
# **Create a Cloud Storage Integration in Snowflake**


A storage integration is a Snowflake object that stores a generated identity and access management (IAM) user for your S3 cloud storage, along with an optional set of allowed or blocked storage locations (i.e. buckets)

<br />

> Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

<br />


1. Choose Roles from the left-hand navigation pane.

```sql
CREATE STORAGE INTEGRATION <integration_name>
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<iam_role>'
  STORAGE_ALLOWED_LOCATIONS = ('s3://<bucket>/<path>/', 's3://<bucket>/<path>/')
  [ STORAGE_BLOCKED_LOCATIONS = ('s3://<bucket>/<path>/', 's3://<bucket>/<path>/') ]
```


```sql
create storage integration phuc_s3
  type = external_stage
  storage_provider = 'S3'
  enabled = true
  storage_aws_role_arn = 'arn:aws:iam::227052876777:role/phuc-snowflake'
  storage_allowed_locations = ('s3://phuc-nguyen/')
//  storage_blocked_locations = ('s3://mybucket1/mypath1/sensitivedata/', 's3://mybucket2/mypath2/sensitivedata/')
;
```

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\snowflake-1.jpg)


<br />

# **Retrieve the AWS IAM User for your Snowflake Account**

1. Execute the DESCRIBE INTEGRATION command to retrieve the ARN for the AWS IAM user that was created automatically for your Snowflake account:

```sql
DESC INTEGRATION <integration_name>;
```

```sql
DESC INTEGRATION phuc_s3;
```

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\snowflake-2.jpg)


2. Record the following values:

> STORAGE_AWS_IAM_USER_ARN : `arn:aws:iam::123456789001:user/abc1-b-self1234`

> STORAGE_AWS_EXTERNAL_ID : `2_rRplaEJeD9Y_SFv81342h1DjTTgZ1Rjo8EZW5CRole==`

<br />
<br />
<br />

# **Grant the IAM User Permissions to Access Bucket Objects**

to configure IAM access permissions for Snowflake in your AWS Management Console so that you can use a S3 bucket to load and unload data

<br />

1. Click the Edit trust relationship button.


![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\role-5.jpg)

<br />

2. Modify the policy document with the DESC STORAGE INTEGRATION output values you recorded.

<br />

3. Click the Update Trust Policy button. The changes are saved.



# **Set up Notification**

Step 1:

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\snowflake-5.jpg)

Step 2:

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\snowflake-6.jpg)

Step 3:


