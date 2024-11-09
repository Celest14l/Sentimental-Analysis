const express = require('express');

const path = require('path');

const {spawn} = require('child_process');

const fs = require("fs");

const app = express();

const bodyParser = require('body-parser');
const { ppid } = require('process');

app.use(bodyParser.urlencoded({extended: true}));

app.use(express.static(path.join(__dirname, "public")));


app.set("view engine", "ejs");

app.get("/", (req, res) => {

    res.render("index");
})

app.post("/process", (req, res) => {

    let dataToSend;

    console.log(req.body.url);

    let url = req.body.url;

    const array = url.split("?v=");

    video_id = array[1];

    console.log(video_id);

    const child = spawn('python', ['extract_comments.py', video_id]);

    child.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    child.stderr.on('data',
    (data) => {
        console.error(`stderr: ${data}`);
    });

    child.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser

        fs.readFile('./public/read.txt', 'utf8', (err, data) => {
            if(err) {
              console.log(err.message);
          } else {
              res.render('results', {text: data});
          }})
    });

});

// app.use(express.cookieParser());

app.get("/", (req, res) =>{
    res.sendFile(path.join(__dirname, "views", "index.html"));
   
});
module.exports = app;

app.listen(3000);

