import mongoose from "mongoose";

export default class ProductRepository {
  constructor(Product) {
    this.Product = Product;
  }

  create(data) {
    return this.Product.create(data);
  }

  findById(id, includeDeleted = false) {
    if (!mongoose.Types.ObjectId.isValid(id)) return null;
    const filter = { _id: id };
    if (!includeDeleted) filter.isDeleted = false;
    return this.Product.findOne(filter);
  }

  update(id, updates) {
    return this.Product.findByIdAndUpdate(id, updates, { new: true, runValidators: true });
  }

  softDelete(id) {
    return this.Product.findByIdAndUpdate(
      id,
      { isDeleted: true, deletedAt: new Date() },
      { new: true }
    );
  }

  findWithFilters({ filters, sort, page, limit }) {
    const skip = (page - 1) * limit;
    return this.Product.find(filters).sort(sort).skip(skip).limit(limit);
  }

  count(filters) {
    return this.Product.countDocuments(filters);
  }
}
