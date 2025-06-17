const fs = require('fs')
//const env = require('dotenv').config({ path: '../.env' })
const path = require('path')
const AWS = require('aws-sdk')
//const ID = process.env.ID
//const SECRET = process.env.SECRET
const BUCKET_NAME = 'kibwa-14'
const MYREGION = 'ap-southeast-2'
const s3 = new AWS.S3({ accessKeyId: process.env.AWS_ACCESS_KEY_ID, secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY, region: MYREGION })
const args = process.argv.slice(2);
const fileType = args[0];

if (fileType === 'text') {
    const fileName = args[1];  // FastAPI에서 넘긴 파일명
    const text = args[2];      // FastAPI에서 넘긴 텍스트

    fs.writeFileSync(fileName, text, { encoding: 'utf-8' });

    const fileContent = fs.readFileSync(fileName);

    const params = {
        Bucket: BUCKET_NAME,
        Key: fileName,
        Body: fileContent,
        ContentType: 'text/plain',
    };

    s3.upload(params, (err, data) => {
        if (err) throw err;
        console.log(`Text file uploaded: ${data.Location}`);
    });
}
else if (fileType === 'mp3') {
    const base64Data = args[1];
    const fileName = 'tts_meeting.mp3';
    const buffer = Buffer.from(base64Data, 'base64');

    fs.writeFileSync(fileName, buffer);

    const params = {
        Bucket: BUCKET_NAME,
        Key: fileName,
        Body: buffer,
        ContentType: 'audio/mpeg',
    };

    s3.upload(params, (err, data) => {
        if (err) throw err;
        console.log(`MP3 file uploaded: ${data.Location}`);
    });
}
else {
    console.error('Unsupported file type:', fileType);
}