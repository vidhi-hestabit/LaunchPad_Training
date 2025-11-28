import { Router } from "express";
import ProductController from "../controllers/product.controller.js";
import { validate } from "../middlewares/validate.js";
import { createProductSchema, updateProductSchema } from "../middlewares/validate.js";

const router = Router();

router.post("/", validate(createProductSchema), ProductController.create);
router.get("/", ProductController.list);
router.get("/:id", ProductController.get);
router.patch("/:id", validate(updateProductSchema), ProductController.update);
router.delete("/:id", ProductController.delete);

export default router;
