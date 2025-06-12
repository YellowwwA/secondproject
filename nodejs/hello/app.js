var express = require("express");
var app = express();

app.get("/", function (req, res) {
    res.send("Hello World - EC2 Deploy");
});

app.listen(8000, function () {
    console.log("8000 Port : Server Started~!!!");
});