// 포트 띄우는 서버
var express = require("express");
const path = require('path');
var app = express();

// 미들웨어
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, 'public')));

// 뷰 엔진 설정 (HTML 렌더링)
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'html')
app.engine('html', require('ejs').renderFile);



app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 라우터
const mainRouter = require('./controllers/mainController');
app.use('/', mainRouter)

app.listen(3000, function () {
    console.log("3000 Port : Server Started~")
});