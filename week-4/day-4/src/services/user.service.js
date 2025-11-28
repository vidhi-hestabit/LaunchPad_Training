import bcrypt from "bcryptjs";

export default class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async createUser(data) {
    
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) throw new Error("Email already registered");

    return this.userRepository.create(data);
  }

  async getUserById(id) {
    const user = await this.userRepository.findById(id);
    if (!user) throw new Error("User not found");
    return user;
  }

  async updateUser(id, updates) {
    const updated = await this.userRepository.update(id, updates);
    if (!updated) throw new Error("User not found");
    return updated;
  }

  async deleteUser(id) {
    const deleted = await this.userRepository.delete(id);
    if (!deleted) throw new Error("User not found");
    return { message: "User deleted successfully" };
  }

  async getUsersPaginated({ page, limit }) {
    return this.userRepository.findPaginated({ page, limit });
  }

  async verifyPassword(email, password) {
    const user = await this.userRepository.findByEmail(email);
    if (!user) throw new Error("Invalid credentials");

    const match = await bcrypt.compare(password, user.password);
    if (!match) throw new Error("Invalid credentials");

    return user;
  }
}
