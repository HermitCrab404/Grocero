//Written by Quintin Wehby
var express = require('express');
var path = require('path');
var app = express();
var index = require("./index.js")
const mysql = require('mysql'); 
var bodyParser = require("body-parser");
var {PythonShell} = require( 'python-shell');
var port = 8080;
var cors = require("cors");

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/index.html'));
  });

app.get('/item', async function(req, res){
      krogerProducts = index.krogerApi(req.body.term, req.body.zipCode);
      samsClubProducts = index.samsClubScraper();
      walgreensProducts = index.walgreensScraper();

      products = krogerProducts + samsClubProducts +WalgreensProducts;

      res.send(products);
    });
app.listen(port);
console.log('server on' + port);