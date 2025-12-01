import express from "express";
import userRouter from "./user.routes.js";
import productRouter from "./product.routes.js";
import emailRoutes from "./email.routes.js";

export default function loadRoutes(app) {
  const router = express.Router();

  router.get("/",(req, res)=>{
    res.status(200).json({status:"ok", message: "Base URL endpoint hit!!!"});
  })
  router.get("/status", (req, res) => {
    res.status(200).json({ status: "ok", message: "Everything is running smoothly." });
  });

  router.use("/email", emailRoutes);

  router.use("/users", userRouter);
  router.use("/products", productRouter);

  router.get("/unknown", (req, res) => {
    res.status(404).json({ error: "Resource not found" });
  });

  app.use("/", router);

  const stack = router.stack.filter((layer) => layer.route || layer.name === "router");
  console.log("Routes loaded:", stack.length);

  return stack.length;
}
