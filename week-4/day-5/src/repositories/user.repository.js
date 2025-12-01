import mongoose from "mongoose";

export default class UserRepository {
  constructor(User) {
    this.User = User;
  }

  create(data) {
    return this.User.create(data);
  }

  findById(id) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;
    return this.User.findById(id);
  }

  update(id, updates) {
    return this.User.findByIdAndUpdate(id, updates, { new: true, runValidators: true });
  }

  delete(id) {
    return this.User.findByIdAndDelete(id);
  }

  // Pagination method
  async findPaginated({ page = 1, limit = 10 }) {
    const skip = (page - 1) * limit;
    const data = await this.User.find().sort({ createdAt: -1 }).skip(skip).limit(limit);
    const total = await this.User.countDocuments();
    return {
      data,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      }
    };
  }

  findByEmail(email) {
    return this.User.findOne({ email });
  }
}
