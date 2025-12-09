import mongoose from "mongoose";

export const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URL);
    console.log("MongoDB Atlas Connected Successfully");
  } catch (err) {
    console.error("MongoDB Error:", err);
    process.exit(1);
  }
};
