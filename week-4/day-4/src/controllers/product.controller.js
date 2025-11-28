import ProductService from "../services/product.service.js";

const svc = new ProductService();

// async wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Validate Mongo ID
const validateId = (id) => {
  if (!/^[0-9a-fA-F]{24}$/.test(id)) {
    const err = new Error("Invalid ID");
    err.status = 400;
    throw err;
  }
  return id;
};

export default class ProductController {
  static create = asyncHandler(async (req, res) => {
    const product = await svc.createProduct(req.body);
    res.status(201).json({ success: true, data: product });
  });

  static get = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const product = await svc.getProductById(id, req.query.includeDeleted === "true");
    res.json({ success: true, data: product });
  });

  static list = asyncHandler(async (req, res) => {
    const result = await svc.searchProducts(req.query);
    res.json({ success: true, data: result.data, meta: result.meta });
  });

  static update = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const updated = await svc.updateProduct(id, req.body);
    res.json({ success: true, data: updated });
  });

  static delete = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const deleted = await svc.deleteProduct(id);
    res.json({ success: true, data: deleted, message: "Product soft-deleted" });
  });
}
