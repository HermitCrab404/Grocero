//Written by Quintin Wehby
var express = require('express');
var path = require('path');
var app = express();
var index = require("./index.js")
var bodyParser = require("body-parser");
var {PythonShell} = require( 'python-shell');
var port = 8080;
var cors = require("cors");

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/grocero.html'));
  });

app.get('/Finder', function(req, res) {
    res.sendFile(path.join(__dirname, '/groceroFinder.html'));
});
//app.get('/', async function(req, res){

        let options = {
        mode: 'text',
        //pythonPath:'', for if its in a venv
        pythonOptions: ['-u'],
        pythonPath:'C:/Users/edweh/venv/Scripts/Python.exe',
        args: [term, location]
        };
        PythonShell.run('./dataCollection/dataCollection.py', options, async function (err, result) {
        if (err)
        groceries = result;
        console.log(groceries)
        });
      res.json(groceries);
//});
app.listen(port);
console.log('server on' + port);

code();