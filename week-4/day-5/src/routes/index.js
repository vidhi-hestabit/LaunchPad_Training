import express from "express";
import userRouter from "./user.routes.js";
import productRouter from "./product.routes.js";
import emailRoutes from "./email.routes.js";
import logger from "../utils/logger.js";

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
function countRoutes(router) {
  let count = 0;

  router.stack.forEach((layer) => {
    if (layer.route) {
      // Direct route (GET, POST, etc.)
      count += 1;
    } else if (layer.name === "router" && layer.handle.stack) {
      // Nested router → recurse
      count += countRoutes(layer.handle);
    }
  });

  return count;
}

const totalRoutes = countRoutes(router);
console.log("Routes loaded:", totalRoutes);

}
