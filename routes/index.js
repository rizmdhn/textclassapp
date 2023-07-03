var express = require("express");
var router = express.Router();
const {spawn} = require('child_process');
const { PythonShell } = require("python-shell");

/* GET home page. */
router.get("/", function (req, res, next) {
  res.render("index");
});

router.post("/classify", function (req, res, next) {
  prediction = [];
  const python = spawn('python', ['public/class.py', req.body.text]);
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    prediction.push(data);
   });
  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    });
   python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    const url = encodeURIComponent(prediction);
    res.redirect("/?prediction=" + url);
  });
    
});

module.exports = router;
