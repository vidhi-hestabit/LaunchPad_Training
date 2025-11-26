export default class UserRepository {
  constructor(UserModel) {
    this.User = UserModel;
  }

  // CREATE
  async create(data) {
    return this.User.create(data);
  }

  // READ
  async findById(id) {
    return this.User.findById(id).lean();
  }

  // PAGINATION (skip/limit OR cursor)
  async findPaginated({ page = 1, limit = 10, status }) {
    const filter = status ? { status } : {};

    const users = await this.User.find(filter)
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .lean();

    return users;
  }
  

  // UPDATE
  async update(id, updates) {
    return this.User.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true,
    }).lean();
  }

  // DELETE
  async delete(id) {
    return this.User.findByIdAndDelete(id);
  }
}
