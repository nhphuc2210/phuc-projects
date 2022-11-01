
# **Configuring Secure Access to Cloud Storage**

## **Agenda**

Creating an IAM Policy

1. Log into the AWS Management Console. <https://signin.aws.amazon.com/signin>

2. From the home dashboard, do 3 steps as below:

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--1.jpg)

3. Choose Policies from the left-hand navigation pane, Click Create Policy.

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--2.jpg)

4. Click the JSON tab, Copy and paste the text into the policy editor


![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--3.jpg)


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "s3:GetObject",
              "s3:GetObjectVersion"
            ],
            "Resource": "arn:aws:s3:::<bucket>/<prefix>/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::<bucket>",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "<prefix>/*"
                    ]
                }
            }
        }
    ]
}
```

*How go get bucket, prefix*

![](https://github.com/nhphuc2210/previous-similar-projects/blob/main/data-pipeline--s3-to-snowflake/.data/grant-access--4.jpg)


