function vote(id, type) {
    fetch('/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, type })
    }).then(response => response.json())
      .then(data => console.log(data));
}

function incrementClick(id) {
    fetch('/increment_click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    }).then(response => response.json())
      .then(data => console.log(data));
}
