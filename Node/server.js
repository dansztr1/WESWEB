const express = require('express');
const ejs = require('ejs');
const app = express();


app.get("/", (request, response) => {
    ejs.renderFile('./home.html', "utf8", (err, html)  => {
        if (err) {
            response.status(500).send("Internal server error")
        }
        response.send(html);
    })
});

app.listen(3000, () => console.log('App Running on http://localhost:3000'))