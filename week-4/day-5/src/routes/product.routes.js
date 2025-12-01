import { Router } from "express";
import ProductController from "../controllers/product.controller.js";
import { validate, createProductSchema, updateProductSchema } from "../middlewares/validate.js";
import { sanitizeXSS } from "../middlewares/security.js";

const router = Router();

router.post("/", validate(createProductSchema), sanitizeXSS, ProductController.create);
router.get("/", ProductController.list);
router.get("/:id", ProductController.get);
router.patch("/:id", validate(updateProductSchema), sanitizeXSS, ProductController.update);
router.delete("/:id", ProductController.delete);

export default router;
