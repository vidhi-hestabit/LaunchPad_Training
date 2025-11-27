import { Router } from "express";
import ProductController from "../controllers/product.controller.js";

const router = Router();

router.post("/", ProductController.create);
router.get("/", ProductController.list);
router.get("/:id", ProductController.get);
router.patch("/:id", ProductController.update);
router.delete("/:id", ProductController.delete);

export default router;
