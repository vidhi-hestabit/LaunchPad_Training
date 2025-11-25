import express from "express";

export default function loadRoutes(app) {
  const router = express.Router();

  router.get("/status", (req, res) => res.json({ status: "ok" }));
  router.get("/users", (req, res) => res.send("Users list"));

  app.use("/", router);

  const stack = router.stack.filter((l) => l.route);
  return stack.length;
}
