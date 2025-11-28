import express from "express";
import UserRepository from "../repositories/user.repository.js";
import UserService from "../services/user.service.js";
import UserController from "../controllers/user.controller.js";
import User from "../models/User.js";
import { createUserSchema, updateUserSchema, validate } from "../middlewares/validate.js";

const router = express.Router();

const userRepository = new UserRepository(User);
const userService = new UserService(userRepository);
const userController = new UserController(userService);

router.post("/",validate(createUserSchema), userController.create);
router.get("/", userController.getAll);
router.get("/:id", userController.getById);
router.put("/:id",validate(updateUserSchema), userController.update);
router.delete("/:id", userController.delete);

export default router;
