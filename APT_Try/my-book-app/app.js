const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const port = 3000;

// データベース接続
const db = new sqlite3.Database('./books.db');

// 初期データベース構築
db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT)");
});

app.use(express.json());
app.use(express.static('public'));

// ルート定義
const booksRouter = require('./routes/books');
app.use('/books', booksRouter);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
