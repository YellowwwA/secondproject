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

let option0 = 'http://13.239.34.242:8080/test';
router.get('/Test', async (req, res) => {
    try {
        const response = await axios.get(option0, {

        });
        res.send(response.data);
    } catch (error) {
        res.status(500).send('FastAPI 호출 실패');
    }
});


let option1 = 'http://13.239.34.242:8080/generate_meeting';
router.get('/generateText', async (req, res) => {
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



module.exports = router;