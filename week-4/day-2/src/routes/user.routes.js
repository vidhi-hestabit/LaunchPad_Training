import express from "express";
import UserRepository from "../repositories/user.repository.js";
import User from "../models/User.js";

const userRepository = new UserRepository(User);
const userRouter = express.Router();
console.log(userRepository);
userRouter.post("/", async (req, res) => {
  try {
    const user = await userRepository.create(req.body);
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


userRouter.get("/", async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const users = await userRepository.findPaginated({ page, limit });
    res.status(200).json({ success: true, data: users });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


userRouter.get("/:id", async (req, res) => {
  try {
    const user = await userRepository.findById(req.params.id);
    res.status(200).json({ success: true, data: user });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


userRouter.put("/:id", async (req, res) => {
  try {
    const updated = await userRepository.update(req.params.id, req.body);
    res.status(200).json({ success: true, data: updated });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


userRouter.delete("/:id", async (req, res) => {
  try {
    await userRepository.delete(req.params.id);
    res.status(200).json({ success: true, message: "User deleted" });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default userRouter;
