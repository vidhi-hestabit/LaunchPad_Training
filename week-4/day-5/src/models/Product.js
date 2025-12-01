import mongoose from "mongoose";

const ProductSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true, index: true },
    description: { type: String, default: "" },
    price: { type: Number, required: true, min: 0, index: true },
    tags: { type: [String], default: [], index: true },
    ratings: [
      { userId: mongoose.Schema.Types.ObjectId, stars: { type: Number, min: 1, max: 5 } }
    ],
    status: { type: String, enum: ["active", "archived"], default: "active", index: true },
    isDeleted: { type: Boolean, default: false, index: true },
    deletedAt: { type: Date, default: null },
  },
  { timestamps: true }
);

// Virtual field
ProductSchema.virtual("averageRating").get(function () {
  if (!this.ratings.length) return 0;
  const sum = this.ratings.reduce((acc, r) => acc + r.stars, 0);
  return +(sum / this.ratings.length).toFixed(2);
});

// Indexes
ProductSchema.index({ status: 1, createdAt: -1 });
ProductSchema.index({ isDeleted: 1, createdAt: -1 });
ProductSchema.index({ price: 1 });

export default mongoose.model("Product", ProductSchema);
