
# **S3 to Glacier**

<br />

##### **Install AWS CLI:** `<link>` : ***<https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>***

<br />

To make sure AWS already installed
```
aws --version
```

Configure
```
aws configure
```

Add to S3 Glacier
```
aws glacier upload-archive --account-id - --vault-name phuc-vault --body archive.zip
```

Get file id
```
aws glacier initiate-job --account-id - --vault-name phuc-vault --job-parameters "{ \"Type\": \"inventory-retrieval\" }"
```

Download from Glacier
```
aws glacier get-job-output --account-id - --vault-name my-vault --job-id zbxcm3Z_3z5UkoroF7SuZKrxgGoDc3RloGduS7Eg-RO47Yc6FxsdGBgf_Q2DK5Ejh18CnTS5XW4_XqlNHS61dsO4CnMW output.json
```



### **Job Descriptions:**

    * ...
    * ...
    * ...

##### **Video in Loom:** `<link>` : ***<https://github.com>***

<br />


