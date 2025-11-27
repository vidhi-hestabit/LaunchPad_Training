export default class UserController {
  constructor(userService) {
    this.userService = userService;
  }

  create = async (req, res, next) => {
    try {
      const user = await this.userService.createUser(req.body);
      res.status(201).json({ success: true, data: user });
    } catch (err) {
      next(err);
    }
  };

  getAll = async (req, res, next) => {
    try {
      const page = parseInt(req.query.page) || 1;
      const limit = parseInt(req.query.limit) || 10;
      const users = await this.userService.getUsersPaginated({ page, limit });
      res.status(200).json({ success: true, ...users });
    } catch (err) {
      next(err);
    }
  };

  getById = async (req, res, next) => {
    try {
      const user = await this.userService.getUserById(req.params.id);
      res.status(200).json({ success: true, data: user });
    } catch (err) {
      next(err);
    }
  };

  update = async (req, res, next) => {
    try {
      const updated = await this.userService.updateUser(req.params.id, req.body);
      res.status(200).json({ success: true, data: updated });
    } catch (err) {
      next(err);
    }
  };

  delete = async (req, res, next) => {
    try {
      const result = await this.userService.deleteUser(req.params.id);
      res.status(200).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  };
}
