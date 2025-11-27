import express from "express";
import UserRepository from "../repositories/user.repository.js";
import UserService from "../services/user.service.js";
import UserController from "../controllers/user.controller.js";
import User from "../models/User.js";

const router = express.Router();

const userRepository = new UserRepository(User);
const userService = new UserService(userRepository);
const userController = new UserController(userService);

router.post("/", userController.create);
router.get("/", userController.getAll);
router.get("/:id", userController.getById);
router.put("/:id", userController.update);
router.delete("/:id", userController.delete);

export default router;
