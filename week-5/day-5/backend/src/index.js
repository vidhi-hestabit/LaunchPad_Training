import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { connectDB } from "./db.js";
import todoRoutes from "./routes/todo.routes.js";
import { healthCheck } from "./health.js";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// DB connect
connectDB();

// Routes
app.get("/api/health", healthCheck);
app.use("/api/todos", todoRoutes);

app.listen(3000, () => console.log("Backend running on port 3000"));
