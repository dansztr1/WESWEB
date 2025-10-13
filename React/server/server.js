const express = require("express");
const app = express();
const cors = require("cors");
const bcrypt = require("bcrypt")
const { DatabaseSync } = require("node:sqlite");
const database = new DatabaseSync("notes.db");
const corsOption = {
  origin: ["http://localhost:5173"],
};


database.exec(`
  CREATE TABLE IF NOT EXISTS data(
    key TEXT PRIMARY KEY,
    value TEXT,
    completed INTEGER
  ) STRICT
`);

app.use(cors(corsOption));
app.use(express.json());

app.get("/getNotes", (req, res) => {
  const query = database.prepare("SELECT * FROM data");
  const allNotes = query.all();

  res.send(allNotes);
});

app.post("/Completed", (req, res) => {
  const { id, completed } = req.body;

  if (!id) {
    return res.status(400).json({ error: "Missing id or title" });
  }

  try {
    const update = database.prepare(
      "UPDATE data SET completed = ? WHERE key = ?"
    );
    const result = update.run(completed, id);

    if (result.changes === 0) {
      return res
        .status(404)
        .json({ error: "Note not found or nothing to update" });
    }

    res.json({ message: "Note updated successfully" });
  } catch (error) {
    console.error("Error updating note:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/delete", (req, res) => {
  const { id } = req.body;

  if (!id) {
    return res.status(400).json({ error: "Missing id" });
  }

  try {
    const update = database.prepare(
      "DELETE from data WHERE key = ?"
    );
    const result = update.run(id);

    res.json({ message: "Note deleted successfully" });
  } catch (error) {
    console.error("Error updating note:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});


app.post("/addNote", (req, res) => {
  const { id, title } = req.body;

  if (!id || !title) {
    return res.status(400).json({ error: "Missing id or title" });
  }

  try {
    const insert = database.prepare(
      "INSERT INTO data (key, value, completed) VALUES (?, ?, 0)"
    );
    insert.run(id, title);

    // res.status(200).json({ message: "Note added successfully", note: { id, title } });
  } catch (error) {
    console.error("Error inserting note:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.listen(3000, () => {
  console.log("Server started on port 3000");
});
