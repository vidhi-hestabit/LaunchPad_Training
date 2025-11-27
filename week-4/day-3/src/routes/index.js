import express from "express";
import userRouter from "./user.routes.js";
import productRouter from "./product.routes.js";

export default function loadRoutes(app) {
  const router = express.Router();

  // Base routes
  router.get("/", (req, res) => {
    res.status(200).json({ message: "Day-1 tasks" });
  });

  router.get("/status", (req, res) => {
    res.status(200).json({ status: "ok", message: "Everything is running smoothly." });
  });

  router.get("/unknown", (req, res) => {
    res.status(404).json({ error: "Resource not found" });
  });

  // Attach user and product routers
  router.use("/users", userRouter);
  router.use("/products", productRouter);

  // Mount all routes to the app
  app.use("/", router);

  // Count only the routes with handlers
  const stack = router.stack.filter((l) => l.route || l.name === "router");
  console.log("Routes loaded:", stack.length);

  return stack.length;
}
