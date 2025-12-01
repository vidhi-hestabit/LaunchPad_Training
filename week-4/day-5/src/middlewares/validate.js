import Joi from "joi";

// Reusable rule: no HTML allowed
const noHTML = Joi.string().custom((value, helpers) => {
  const htmlRegex = /<\/?[a-z][\s\S]*>/i;
  if (htmlRegex.test(value)) {
    return helpers.message("HTML tags are not allowed");
  }
  return value;
}, "No HTML rule");

// User schemas
export const createUserSchema = Joi.object({
  firstName: noHTML.min(2).max(50).required(),
  lastName: noHTML.min(2).max(50).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(6).max(128).required(),
  status: Joi.string().valid("active", "inactive").optional()
});

export const updateUserSchema = Joi.object({
  firstName: noHTML.min(2).max(50),
  lastName: noHTML.min(2).max(50),
  email: Joi.string().email(),
  password: Joi.string().min(6).max(128),
  status: Joi.string().valid("active", "inactive")
}).min(1);

// Product schemas
export const createProductSchema = Joi.object({
  name: noHTML.min(2).max(100).required(),
  description: noHTML.allow("").optional(),
  price: Joi.number().min(0).required(),
  tags: Joi.array().items(noHTML),
  status: Joi.string().valid("active", "inactive").optional()
});

export const updateProductSchema = Joi.object({
  name: noHTML.min(2).max(100),
  description: noHTML.allow(""),
  price: Joi.number().min(0),
  tags: Joi.array().items(noHTML),
  status: Joi.string().valid("active", "inactive")
}).min(1);

// Validation middleware
export const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      success: false,
      errors: error.details.map((d) => d.message),
    });
  }
  next();
};
