import express from "express";

export default function loadRoutes(app) {
  const router = express.Router();

  router.get("/", (req, res) => {
    res.status(200).json({ message: "Day-1 tasks" });
  });

  router.get("/status", (req, res) => {
    res.status(200).json({ status: "ok", message: "Everything is running smoothly." });
  });

  router.get("/users", (req, res) => {
    res.status(201).json({ message: "Users list created" });
  });

  router.get("/unknown", (req, res) => {
    res.status(404).json({ error: "Resource not found" });
  });

  
  app.use("/", router);

  const stack = router.stack.filter((l) => l.route);
  console.log("Routes loaded:", stack.length);
  return stack.length;
}
