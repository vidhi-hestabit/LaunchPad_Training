import { Router } from "express";
import UserController from "../controllers/user.controller.js";
import { validate, createUserSchema, updateUserSchema } from "../middlewares/validate.js";

const router = Router();

router.post("/", validate(createUserSchema), UserController.create);
router.get("/", UserController.list);
router.get("/:id", UserController.get);
router.put("/:id", validate(updateUserSchema), UserController.update);
router.delete("/:id", UserController.delete);

export default router;
