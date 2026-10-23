-- only when not logged in through the aws cli
CREATE OR REPLACE SECRET (
    TYPE S3,
    KEY_ID 'XXX',
    SECRET 'YYY',
    REGION 'eu-central-1', 
    SCOPE 's3://test-data-matthias'
)

-- roughly 2,5 GB
SELECT * EXCLUDE payload
FROM read_json('s3://test-data-matthias/github/*.json.gz')
LIMIT 10;

SELECT actor.login, actor.url FROM read_json('s3://test-data-matthias/github/*.json.gz') LIMIT 10


