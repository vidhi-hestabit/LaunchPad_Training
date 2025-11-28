import Joi from "joi";

// User validation schemas
export const createUserSchema = Joi.object({
  firstName: Joi.string().min(2).max(50).required(),
  lastName: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(6).max(128).required(),
  status: Joi.string().valid("active", "inactive").optional()
});

export const updateUserSchema = Joi.object({
  firstName: Joi.string().min(2).max(50),
  lastName: Joi.string().min(2).max(50),
  email: Joi.string().email(),
  password: Joi.string().min(6).max(128),
  status: Joi.string().valid("active", "inactive")
}).min(1);

// Product validation schemas
export const createProductSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  description: Joi.string().allow("").optional(),
  price: Joi.number().min(0).required(),
  tags: Joi.array().items(Joi.string()).optional(),
  status: Joi.string().valid("active", "inactive").optional()
});

export const updateProductSchema = Joi.object({
  name: Joi.string().min(2).max(100),
  description: Joi.string().allow(""),
  price: Joi.number().min(0),
  tags: Joi.array().items(Joi.string()),
  status: Joi.string().valid("active", "inactive")
}).min(1);

// Middleware generator
export const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      success: false,
      errors: error.details.map((d) => d.message)
    });
  }
  next();
};
