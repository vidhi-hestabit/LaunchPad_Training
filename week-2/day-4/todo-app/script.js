   // Theme
    function toggleTheme() {
      const html = document.documentElement;
      const theme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
      document.getElementById('theme-icon').textContent = theme === 'dark' ? '🌙' : '☀️';
    }

    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark') {
      document.getElementById('theme-icon').textContent = '🌙';
    }

    // Todo App
    const input = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');
    const list = document.getElementById('todo-list');
    const totalTasks = document.getElementById('total-tasks');
    const completedTasks = document.getElementById('completed-tasks');
    const editModal = document.getElementById('edit-modal');
    const editInput = document.getElementById('edit-input');

    let todos = JSON.parse(localStorage.getItem('todos')) || [];
    let editingId = null;

    // Add todo
    addBtn.addEventListener('click', addTodo);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') addTodo();
    });

    function addTodo() {
      const text = input.value.trim();
      if (!text) return;

      const newTodo = {
        id: Date.now(),
        text: text,
        completed: false
      };

      todos.push(newTodo);
      saveTodos();
      render();
      input.value = '';
    }

    // Toggle complete
    function toggleComplete(id) {
      const todo = todos.find(t => t.id == id);
      if (todo) {
        todo.completed = !todo.completed;
        saveTodos();
        render();
      }
    }

    // Open edit modal
    function openEditModal(id) {
      const todo = todos.find(t => t.id == id);
      if (todo) {
        editingId = id;
        editInput.value = todo.text;
        editModal.classList.add('active');
        editInput.focus();
      }
    }

    // Close modal
    function closeModal() {
      editModal.classList.remove('active');
      editingId = null;
      editInput.value = '';
    }

    // Save edit
    function saveEdit() {
      const newText = editInput.value.trim();
      if (!newText) return;

      const todo = todos.find(t => t.id == editingId);
      if (todo) {
        todo.text = newText;
        saveTodos();
        render();
        closeModal();
      }
    }

    // Delete todo
    function deleteTodo(id) {
      if (confirm('Are you sure you want to delete this task?')) {
        todos = todos.filter(t => t.id != id);
        saveTodos();
        render();
      }
    }

    // Save to localStorage
    function saveTodos() {
      localStorage.setItem('todos', JSON.stringify(todos));
    }

    // Render todos
    function render() {
      list.innerHTML = '';

      if (todos.length === 0) {
        list.innerHTML = `
          <div class="empty-state">
            <div class="empty-state-icon">📝</div>
            <p>No tasks yet. Add one to get started!</p>
          </div>
        `;
      } else {
        todos.forEach(todo => {
          const li = document.createElement('li');
          li.className = 'todo-item';
          li.innerHTML = `
            <input 
              type="checkbox" 
              class="todo-checkbox" 
              ${todo.completed ? 'checked' : ''}
              onchange="toggleComplete(${todo.id})"
            />
            <span class="todo-text ${todo.completed ? 'completed' : ''}">${escapeHtml(todo.text)}</span>
            <div class="todo-actions">
              <button class="btn btn-edit" onclick="openEditModal(${todo.id})">Edit</button>
              <button class="btn btn-delete" onclick="deleteTodo(${todo.id})">Delete</button>
            </div>
          `;
          list.appendChild(li);
        });
      }

      updateStats();
    }

    // Update statistics
    function updateStats() {
      const total = todos.length;
      const completed = todos.filter(t => t.completed).length;
      totalTasks.textContent = `Total: ${total}`;
      completedTasks.textContent = `Completed: ${completed}`;
    }

    // Escape HTML
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }

    // Close modal on overlay click
    editModal.addEventListener('click', (e) => {
      if (e.target === editModal) closeModal();
    });

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && editModal.classList.contains('active')) {
        closeModal();
      }
    });

    // Save edit on Enter key
    editInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') saveEdit();
    });

    // Initial render
    render();