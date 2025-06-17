const express = require("express");
const router = express.Router();
const axios = require("axios");

// 메인 페이지 렌더링
router.get("/", (req, res) => {
    res.render("index");
});

router.get('/hello', (req, res) => {
    res.send({ data: 'Hello World!!' });
})


let option1 = 'http://13.236.151.41:8080/generate_meeting';
router.get('/generate_meeting', async (req, res) => {
    try {
        const { keyword, num, textlength } = req.query;
        const response = await axios.get(option1, {
            params: { keyword, num, textlength }
        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send('FastAPI 호출 실패');
    }
});

let option2 = 'http://13.236.151.41:8080/tts_meeting';
router.get('/tts_meeting', async (req, res) => {
    try {
        const { keyword, num, textlength } = req.query;
        const response = await axios.get(option2, {
            params: {}
        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send('FastAPI 호출 실패');
    }
});

let option3 = 'http://13.236.151.41:8080/stt_meeting';
router.get('/stt_meeting', async (req, res) => {
    try {
        const { keyword, num, textlength } = req.query;
        const response = await axios.get(option3, {
            params: {}
        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send('FastAPI 호출 실패');
    }
});


let option4 = 'http://13.236.151.41:8080/summarize_meetingtext';
router.get('/summarize_meetingtext', async (req, res) => {
    try {
        const { keyword, num, textlength } = req.query;
        const response = await axios.get(option4, {
            params: {}
        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send('FastAPI 호출 실패');
    }
});


module.exports = router;