import UserService from "../services/user.service.js";

const svc = new UserService();

const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

const validateId = (id) => {
  if (!/^[0-9a-fA-F]{24}$/.test(id)) {
    const err = new Error("Invalid ID");
    err.status = 400;
    throw err;
  }
  return id;
};

export default class UserController {
  static create = asyncHandler(async (req, res) => {
    const user = await svc.createUser(req.body);
    res.status(201).json({ success: true, data: user });
  });

  static get = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const user = await svc.getUserById(id);
    res.json({ success: true, data: user });
  });

  static list = asyncHandler(async (req, res) => {
    const page = Number(req.query.page) || 1;
    const limit = Number(req.query.limit) || 10;

    const result = await svc.getUsersPaginated({ page, limit });
    res.json({ success: true, data: result.data, meta: result.meta });
  });

  static update = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const updated = await svc.updateUser(id, req.body);
    res.json({ success: true, data: updated });
  });

  static delete = asyncHandler(async (req, res) => {
    const id = validateId(req.params.id);
    const result = await svc.deleteUser(id);
    res.json({ success: true, data: result, message: result.message });
  });
}
