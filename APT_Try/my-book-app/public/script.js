document.getElementById('add-book-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('book-title').value;
    fetch('/books', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title })
    })
    .then(response => response.json())
    .then(book => {
      const li = document.createElement('li');
      li.textContent = book.title;
      li.addEventListener('click', () => {
        alert(`詳細画面\nタイトル: ${book.title}`);
      });
      document.getElementById('book-list').appendChild(li);
    });
  });
  