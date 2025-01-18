const express = require('express');
const router = express.Router();
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./books.db');

// 本の一覧取得
router.get('/', (req, res) => {
  db.all("SELECT * FROM books", [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

// 本の追加
router.post('/', (req, res) => {
  const { title } = req.body;
  db.run("INSERT INTO books (title) VALUES (?)", [title], function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ id: this.lastID, title });
  });
});

module.exports = router;
