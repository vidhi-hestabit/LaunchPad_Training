export default class ProductRepository {
  constructor(ProductModel) {
    this.Product = ProductModel;
  }
  // CREATE
  async create(data) {
    return this.Product.create(data);
  }
  // FIND BY ID
  async findById(id) {
    return this.Product.findById(id);
  }
  // PAGINATION
  async findPaginated({ page = 1, limit = 10, status }) {
    const filter = status ? { status } : {};
    const products = await this.Product.find(filter)
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .lean();
    return products;
  }
  // UPDATE
  async update(id, updates) {
    return this.Product.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true,
    });
  }
  // DELETE
  async delete(id) {
    return this.Product.findByIdAndDelete(id);
  }
}
