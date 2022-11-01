
# **Create the IAM Role in AWS**

1. Choose Roles from the left-hand navigation pane.

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake\.data\role-1.jpg)


2. Select Another AWS account as the trusted entity type:

    *Select the Require external ID option. Enter a dummy ID such as 0000. Later, you will modify the trusted relationship and specify the external ID for your Snowflake stage. An external ID is required to grant access to your AWS resources (i.e. S3) to a third party (i.e. Snowflake).*


![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--2.jpg)


3. Select the policy you created in Step 1

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--3.jpg)


4. Enter a name and description for the role, and click the Create role button.

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--3.jpg)

You have now created an IAM policy for a bucket, created an IAM role, and attached the policy to the role.


5. Save your ARN 

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--4.jpg)

