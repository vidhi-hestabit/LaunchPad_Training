import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Mongo connection
mongoose
  .connect(process.env.MONGO_URL)
  .then(() => console.log("Connected to Mongo"))
  .catch((err) => console.error("Mongo Error:", err));

// Schema
const TodoSchema = new mongoose.Schema({
  task: String,
});

const Todo = mongoose.model("Todo", TodoSchema);

// Routes
app.get("/todos", async (req, res) => {
  const todos = await Todo.find();
  res.json(todos);
});

app.post("/todos", async (req, res) => {
  const todo = await Todo.create(req.body);
  res.json(todo);
});

app.listen(4000, () => console.log("Server running on 4000"));
