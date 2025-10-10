const express = require("express");
const app = express();
const cors = require("cors");
const corsOption = {
    origin: ["http://localhost:5173"]
}

app.use(cors(corsOption))

app.get("/api", (req, res) => {
    res.json({"Fruits": ["Apple", "Orange", "Banana"]})
});

app.listen(3000, () => {
    console.log("Server started on port 3000")
})