const fs =  require('fs')
const http = require('http')

const express = require('express');
const path = require('path');

// console.log('hey')

// const server = http.createServer(function(req,res){
//     res.end("hlo world");
// })

// server.listen(3000);

const app = express();

// app.use(function(req, res, next){
//     console.log('middleware running');
//     next();

// })

app.use(express.json());
app.use(express.urlencoded({extended:true}));

app.use(express.static(path.join(__dirname, 'public')));

app.set('view engine','ejs');

// routes - URL sort of

app.get("/", function(req,res){
    res.render ("index");
});

app.get("/profile", function(req, res){
    res.send("coach")
});

app.get("/route1", function(req, res){
    res.send("route1")
});



app.listen(3000);