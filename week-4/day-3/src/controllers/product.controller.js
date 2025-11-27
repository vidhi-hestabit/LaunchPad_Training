import ProductService from "../services/product.service.js";

const svc = new ProductService();

export default class ProductController {
  static async create(req, res, next) {
    const { name, price } = req.body;
    if (!name || typeof name !== "string") return res.status(400).json({ error: "Name required" });
    if (price == null || typeof price !== "number" || price <= 0) return res.status(400).json({ error: "Valid price required" });

    try {
      const product = await svc.createProduct(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (err) { next(err); }
  }

  static async get(req, res, next) {
    const { id } = req.params;
    if (!id || !/^[0-9a-fA-F]{24}$/.test(id)) return res.status(400).json({ error: "Invalid ID" });

    try {
      const product = await svc.getProductById(id, req.query.includeDeleted === "true");
      res.json({ success: true, data: product });
    } catch (err) { next(err); }
  }

  static async list(req, res, next) {
    try {
      const result = await svc.searchProducts(req.query);
      res.json({ success: true, data: result.data, meta: result.meta });
    } catch (err) { next(err); }
  }

  static async update(req, res, next) {
    const { id } = req.params;
    if (!id || !/^[0-9a-fA-F]{24}$/.test(id)) return res.status(400).json({ error: "Invalid ID" });

    try {
      const updated = await svc.updateProduct(id, req.body);
      res.json({ success: true, data: updated });
    } catch (err) { next(err); }
  }

  static async delete(req, res, next) {
    const { id } = req.params;
    if (!id || !/^[0-9a-fA-F]{24}$/.test(id)) return res.status(400).json({ error: "Invalid ID" });

    try {
      const deleted = await svc.deleteProduct(id);
      res.json({ success: true, data: deleted, message: "Product soft-deleted" });
    } catch (err) { next(err); }
  }
}
