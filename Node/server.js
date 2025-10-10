const express = require("express");
const session = require("express-session");
const app = express();

app.set("view engine", "ejs");


app.use(
  session({
    secret: "123123712",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }, // secure should be true in production with HTTPS
  })
);

app.use(express.static("public"));

app.get("/", (req, res) => {
  res.render("index", (user = req.session.username));
});

app.get("/login", (req, res) => {
  res.render("login", (user = req.session.username));
});

app.listen(3000, () => console.log("App Running on http://localhost:3000"));
