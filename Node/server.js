const express = require('express');
const sqlite = require('node:sqlite');
const app = express();
const { DatabaseSync } = require('node:sqlite');
const database = new DatabaseSync(':memory:');

app.set('view engine', 'ejs');
app.use(express.static('public'));




app.get('/', (req, res) => {
    res.render('index');
});

app.get('/add', (req, res) => {
    res.render('add');
});

app.listen(3000, () => console.log('App Running on http://localhost:3000'))