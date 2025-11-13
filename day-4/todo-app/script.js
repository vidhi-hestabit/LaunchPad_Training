// ===== Utilities =====
function saveTodos(todos) {
  localStorage.setItem('todos', JSON.stringify(todos));
}

function getTodos() {
  return JSON.parse(localStorage.getItem('todos')) || [];
}

// ===== Main App =====
const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const list = document.getElementById('todo-list');

let todos = getTodos();
renderTodos();

// Add new todo
addBtn.addEventListener('click', () => {
  const text = input.value.trim();
  if (!text) return;

  const newTodo = { id: Date.now(), text };
  todos.push(newTodo);
  saveTodos(todos);
  renderTodos();
  input.value = '';
});

// Edit or delete
list.addEventListener('click', (e) => {
  const id = e.target.closest('li').dataset.id;

  if (e.target.classList.contains('delete')) {
    todos = todos.filter(todo => todo.id != id);
  } else if (e.target.classList.contains('edit')) {
    const newText = prompt('Edit task:', todos.find(t => t.id == id).text);
    if (newText) todos.find(t => t.id == id).text = newText;
  }

  saveTodos(todos);
  renderTodos();
});

// Render function
function renderTodos() {
  list.innerHTML = '';
  todos.forEach(todo => {
    const li = document.createElement('li');
    li.dataset.id = todo.id;
    li.innerHTML = `
      <span>${todo.text}</span>
      <div>
        <button class="edit">Edit</button>
        <button class="delete">Delete</button>
      </div>`;
    list.appendChild(li);
  });
}

// ===== Error Handling =====
try {
  renderTodos();
} catch (err) {
  console.error('Render error:', err);
}

