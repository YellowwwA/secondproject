const fs = require('fs')
//const env = require('dotenv').config({ path: '../.env' })

const AWS = require('aws-sdk')
//const ID = process.env.ID
//const SECRET = process.env.SECRET
const BUCKET_NAME = 'kibwa-14'
const MYREGEION = 'ap-southeast-2'
const s3 = new AWS.S3({ accessKeyId: process.env.AWS_ACCESS_KEY_ID, secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY, region: MYREGION })


const params = {
    Bucket: BUCKET_NAME,
    Key: s3Key,
};

s3.getObject(params, (err, data) => {
    if (err) {
        throw err;
    }

    if (contentType === 'text') {
        const text = data.Body.toString('utf-8');
        process.stdout.write(text);
    } else if (contentType === 'mp3') {
        process.stdout.write(data.Body);
    } else {
        console.error('Unsupported content type:', contentType);
        process.exit(1);
    }
})
