import bcrypt from "bcryptjs";

export default class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async createUser(data) {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      const err = new Error("Email already registered");
      err.status = 400;
      throw err;
    }

    return this.userRepository.create(data);
  }

  async getUserById(id) {
    const user = await this.userRepository.findById(id);
    if (!user) {
      const err = new Error("User not found");
      err.status = 404;
      throw err;
    }
    return user;
  }

  async updateUser(id, updates) {
    const exists = await this.getUserById(id);
    return this.userRepository.update(id, updates);
  }

  async deleteUser(id) {
    const exists = await this.getUserById(id);
    await this.userRepository.delete(id);
    return { message: "User deleted successfully" };
  }

  async getUsersPaginated({ page, limit }) {
    return this.userRepository.findPaginated({ page, limit });
  }

  async verifyPassword(email, password) {
    const user = await this.userRepository.findByEmail(email);
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
