import mongoose from "mongoose";

const ProductSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    price: {
      type: Number,
      min: 0,
      required: true,
    },
    ratings: [
      {
        userId: mongoose.Schema.Types.ObjectId,
        stars: { type: Number, min: 1, max: 5 },
      },
    ],
    status: {
      type: String,
      enum: ["active", "archived"],
      default: "active",
    },
  },
  { timestamps: true }
);


ProductSchema.virtual("averageRating").get(function () {
  if (!this.ratings?.length) return 0;
  const sum = this.ratings.reduce((acc, r) => acc + r.stars, 0);
  return (sum / this.ratings.length).toFixed(2);
});


ProductSchema.index({ status: 1, createdAt: -1 });


ProductSchema.pre("save", function (next) {
  this.name = this.name.trim();
});


export default mongoose.model("Product", ProductSchema);
