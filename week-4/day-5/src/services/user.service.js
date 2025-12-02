import bcrypt from "bcryptjs";
import User from "../models/User.js"
import UserRepository from "../repositories/user.repository.js";


const repo = new UserRepository(User);

export default class UserService {
  
  async createUser(data) {
    const existing = await this.repo.findByEmail(data.email);
    if (existing) {
      const err = new Error("Email already registered");
      err.status = 400;
      throw err;
    }

    return repo.create(data);
  }

  async getUserById(id) {
    const user = await this.repo.findById(id);
    if (!user) {
      const err = new Error("User not found");
      err.status = 404;
      throw err;
    }
    return user;
  }

  async updateUser(id, updates) {
    const exists = await this.getUserById(id);
    return repo.update(id, updates);
  }

  async deleteUser(id) {
    const exists = await this.getUserById(id);
    await repo.delete(id);
    return { message: "User deleted successfully" };
  }

  async getUsersPaginated({ page, limit }) {
    return repo.findPaginated({ page, limit });
  }

  async verifyPassword(email, password) {
    const user = await this.repo.findByEmail(email);
    if (!user) {
      const err = new Error("Invalid credentials");
      err.status = 401;
      throw err;
    }

    const match = await bcrypt.compare(password, user.password);
    if (!match) {
      const err = new Error("Invalid credentials");
      err.status = 401;
      throw err;
    }

    return user;
  }
}
