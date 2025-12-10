import { useEffect, useState } from "react";
import { api } from "./api";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");

  const loadTodos = async () => {
    try {
      const res = await api.get("/todos");
      console.log("API Response:", res.data);

      const todosArray = Array.isArray(res.data) ? res.data : res.data?.data || [];
      setTodos(todosArray);

    } catch (err) {
      console.error("Failed to load todos:", err);
      setTodos([]); // fallback to empty array
    }
  };

  const createTodo = async () => {
    if (!text) return;
    try {
      await api.post("/todos", { text });
      setText("");
      loadTodos();
    } catch (err) {
      console.error("Failed to create todo:", err);
    }
  };

  const toggleTodo = async (id) => {
    try {
      await api.put(`/todos/${id}`);
      loadTodos();
    } catch (err) {
      console.error("Failed to toggle todo:", err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      loadTodos();
    } catch (err) {
      console.error("Failed to delete todo:", err);
    }
  };

  useEffect(() => {
    loadTodos();
  }, []);

  return (
    <div style={{ width: "400px", margin: "40px auto", fontFamily: "Arial" }}>
      <h2>Todo App</h2>

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter todo"
      />
      <button onClick={createTodo}>Add</button>

      <ul>
        {Array.isArray(todos) && todos.map((t) => (
          <li key={t._id}>
            <span
              onClick={() => toggleTodo(t._id)}
              style={{
                cursor: "pointer",
                textDecoration: t.completed ? "line-through" : "none"
              }}
            >
              {t.text}
            </span>
            <button onClick={() => deleteTodo(t._id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
