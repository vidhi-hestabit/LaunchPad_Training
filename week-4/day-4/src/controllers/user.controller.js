import { createUserSchema, updateUserSchema } from "../middlewares/validate.js";

export default class UserController {
  constructor(userService) {
    this.userService = userService;
  }

  static asyncHandler = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

  create = UserController.asyncHandler(async (req, res) => {
    await createUserSchema.validateAsync(req.body, { abortEarly: true });
    const user = await this.userService.createUser(req.body);
    res.status(201).json({ success: true, data: user });
  });

  getAll = UserController.asyncHandler(async (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const users = await this.userService.getUsersPaginated({ page, limit });
    res.status(200).json({ success: true, data: users.data, meta: users.meta });
  });
  
  getById = UserController.asyncHandler(async (req, res) => {
    const user = await this.userService.getUserById(req.params.id);
    res.status(200).json({ success: true, data: user });
  });

  update = UserController.asyncHandler(async (req, res) => {
    await updateUserSchema.validateAsync(req.body, { abortEarly: false });
    const updated = await this.userService.updateUser(req.params.id, req.body);
    res.status(200).json({ success: true, data: updated });
  });
  
  delete = UserController.asyncHandler(async (req, res) => {
    const result = await this.userService.deleteUser(req.params.id);
    res.status(200).json({ success: true, message: result.message });
  });
}
