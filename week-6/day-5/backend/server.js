require("dotenv").config();
const express = require("express");
const axios = require("axios");
const cors = require("cors");
const mongoose = require("mongoose");

const app = express();
app.use(cors());
app.use(express.json());

const ML_URL = process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";
const MONGO_URI = process.env.MONGO_URI;

// Connect to MongoDB
mongoose.connect(MONGO_URI)
.then(() => console.log("✅ MongoDB connected"))
.catch(err => console.error("❌ MongoDB connection error:", err));

// Define schema
const predictionSchema = new mongoose.Schema({
  name: String,
  age: Number,
  experience_years: Number,
  tech_count: Number,
  primary_tech: String,
  education_level: String,
  predicted_package_lpa: Number,
  request_id: String,
  timestamp: { type: Date, default: Date.now }
});

const Prediction = mongoose.model("Prediction", predictionSchema);

// Prediction endpoint
app.post("/api/predict", async (req, res) => {
  try {
    const { name, age, experience_years, tech_count, primary_tech, education_level } = req.body;

    if (!name || !age || experience_years === undefined || !tech_count || !primary_tech || !education_level) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    const response = await axios.post(`${ML_URL}/predict`, {
      age, experience_years, tech_count, primary_tech, education_level
    });

    const data = response.data;

    // Save prediction to MongoDB
    const savedPrediction = await Prediction.create({
      name,
      age,
      experience_years,
      tech_count,
      primary_tech,
      education_level,
      predicted_package_lpa: data.predicted_package_lpa,
      request_id: data.request_id,
      timestamp: data.timestamp
    });

    res.json(data);

  } catch (err) {
    console.error("Prediction error:", err.response?.data || err.message);
    res.status(500).json({ error: "Prediction failed" });
  }
});

// Stats endpoint
app.get("/api/stats", async (req, res) => {
  try {
    const count = await Prediction.countDocuments();
    const avg = await Prediction.aggregate([
      { $group: { _id: null, avgPackage: { $avg: "$predicted_package_lpa" } } }
    ]);

    res.json({
      total_predictions: count,
      average_prediction: avg[0]?.avgPackage || 0
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch stats" });
  }
});

app.listen(process.env.PORT || 5000, () => {
  console.log("🚀 Backend running on port 5000");
});
