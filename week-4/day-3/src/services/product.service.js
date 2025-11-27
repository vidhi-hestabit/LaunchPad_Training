import ProductRepository from "../repositories/product.repository.js";
import Product from "../models/Product.js"


const repo = new ProductRepository(Product);

export default class ProductService {
  createProduct(data) {
    if (!data.name || data.price === undefined) {
      const err = new Error("Name and price are required");
      err.status = 400;
      err.code = "VALIDATION_ERROR";
      throw err;
    }
    return repo.create(data);
  }

  async getProductById(id, includeDeleted = false) {
    const product = await repo.findById(id, includeDeleted);
    if (!product) {
      const err = new Error("Product not found");
      err.status = 404;
      err.code = "NOT_FOUND";
      throw err;
    }
    return product;
  }

  async updateProduct(id, updates) {
    await this.getProductById(id, true);
    return repo.update(id, updates);
  }

  async deleteProduct(id) {
    const product = await this.getProductById(id, true);
    if (product.isDeleted) return product;
    return repo.softDelete(id);
  }

  async searchProducts(query) {
    const {
      page = 1,
      limit = 10,
      search,
      minPrice,
      maxPrice,
      tags,
      status,
      includeDeleted = false,
      sort = "createdAt:desc",
    } = query;

    const filters = {};

    if (!JSON.parse(includeDeleted)) filters.isDeleted = false;
    if (search) {
      const re = new RegExp(search, "i");
      filters.$or = [{ name: re }, { description: re }, { tags: re }];
    }
    if (minPrice || maxPrice) filters.price = {};
    if (minPrice) filters.price.$gte = Number(minPrice);
    if (maxPrice) filters.price.$lte = Number(maxPrice);
    if (tags) filters.tags = { $in: tags.split(",") };
    if (status) filters.status = status;

    const [field, dir] = sort.split(":");
    const sortObj = { [field]: dir === "asc" ? 1 : -1 };

    const data = await repo.findWithFilters({ filters, sort: sortObj, page: Number(page), limit: Number(limit) });
    const total = await repo.count(filters);

    return { data, meta: { page: Number(page), limit: Number(limit), total, totalPages: Math.ceil(total / limit) } };
  }
}
