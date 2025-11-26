import express from "express";
import ProductRepository from "../repositories/product.repository.js";
import Product from "../models/Product.js";

const productRouter = express.Router();
const productRepository = new ProductRepository(Product);

productRouter.post("/", async (req, res) => {
  try {
    const product = await productRepository.create(req.body);
    res.json({ success: true, data: product });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});



productRouter.get("/:id", async (req, res) => {
  try {
    const product = await productRepository.findById(req.params.id);
    res.json({ success: true, data: product });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});



productRouter.get("/", async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const result = await productRepository.findPaginated({ page, limit });

    res.json({ success: true, data: result });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


productRouter.put("/:id", async (req, res) => {
  try {
    const updated = await productRepository.update(req.params.id, req.body);
    res.json({ success: true, data: updated });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});


productRouter.delete("/:id", async (req, res) => {
  try {
    await productRepository.delete(req.params.id);
    res.json({ success: true, message: "Product deleted successfully" });
  } catch (error) {
    res.status(400).json({ success: false, error: error.message });
  }
});

export default productRouter;
