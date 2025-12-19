"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Moon, Sun } from "lucide-react";

export default function Home() {
  const [dark, setDark] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark-mode");
    } else {
      document.documentElement.classList.remove("dark-mode");
    }
  }, [dark]);

  const [form, setForm] = useState({
    name: "",
    age: "",
    experience_years: "",
    tech_count: "",
    primary_tech: "Python",
    education_level: "Bachelors",
  });

  const submit = async () => {
    setLoading(true);
    setResult(null);
    const res = await fetch("http://localhost:5000/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        age: Number(form.age),
        experience_years: Number(form.experience_years),
        tech_count: Number(form.tech_count),
        primary_tech: form.primary_tech,
        education_level: form.education_level,
      }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* NAVBAR */}
      <header
        className="fixed top-0 w-full z-50 backdrop-blur border-b"
        style={{ backgroundColor: "var(--header-bg)" }}
      >
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="font-bold text-xl">Package Predictor</h1>
          <div className="flex items-center gap-6">
            <nav className="hidden md:flex gap-6 text-sm font-medium">
              <a href="#features" className="accent hover:underline">
                Features
              </a>
              <a href="#predict" className="accent hover:underline">
                Predict
              </a>
              <a href="#about" className="accent hover:underline">
                About
              </a>
            </nav>
            <button
              onClick={() => setDark(!dark)}
              className="p-2 rounded-full border"
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>

      {/* HERO */}
      <section
        className="pt-32 pb-24 text-white"
        style={{ background: "linear-gradient(to bottom right, #2563eb, #4f46e5)" }}
      >
        <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-extrabold leading-tight">
              Predict Your{" "}
              <span style={{ color: "#facc15" }}>Career Package</span>
              <br /> Using Machine Learning
            </h2>
            <p className="mt-6 text-lg text-blue-100">
              Data-driven salary prediction using experience, skills, and education.
              Built like a real ML product.
            </p>
            <a
              href="#predict"
              className="inline-block mt-8 px-6 py-3 rounded-lg shadow font-semibold"
              style={{ backgroundColor: "var(--accent)", color: "#fff" }}
            >
              Try Prediction →
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            className="hidden md:block p-6 rounded-2xl"
            style={{ backgroundColor: "rgba(255,255,255,0.1)" }}
          >
            <p>✔ Used by ML Engineers ✔ Production-ready pipeline ✔ Real-world inference API</p>
          </motion.div>
        </div>
      </section>

      {/* FEATURES */}
      <section id="features" className="py-24">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h3 className="text-3xl font-bold mb-12">Why This Platform?</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              ["ML-Driven", "Trained using real-world features"],
              ["Fast API", "Production-grade inference service"],
              ["Explainable", "Feature-aware predictions"],
            ].map(([title, desc]) => (
              <div
                key={title}
                className="card p-6 rounded-xl shadow"
              >
                <h4 className="font-semibold text-lg mb-2">{title}</h4>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem" }}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* PREDICTION APP */}
      <section id="predict" className="py-24">
        <div className="max-w-xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            className="card p-8 rounded-2xl shadow-xl"
          >
            <h3 className="text-2xl font-bold mb-6 text-center">Salary Prediction</h3>
            <input
              placeholder="Candidate Name"
              type="text"
              className="w-full px-4 py-2 rounded-lg border mb-4 bg-transparent"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <div className="space-y-4">
              {[
                ["Age", "age"],
                ["Experience (Years)", "experience_years"],
                ["Tech Count", "tech_count"],
              ].map(([label, key]) => (
                <input
                  key={key}
                  placeholder={label}
                  type="number"
                  className="w-full px-4 py-2 rounded-lg border bg-transparent"
                  value={form[key]}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                />
              ))}

              <select
                className="w-full px-4 py-2 rounded-lg border bg-transparent"
                value={form.primary_tech}
                onChange={(e) =>
                  setForm({ ...form, primary_tech: e.target.value })
                }
              >
                <option>Python</option>
                <option>Java</option>
                <option>JavaScript</option>
              </select>

              <select
                className="w-full px-4 py-2 rounded-lg border bg-transparent"
                value={form.education_level}
                onChange={(e) =>
                  setForm({ ...form, education_level: e.target.value })
                }
              >
                <option>Bachelors</option>
                <option>Masters</option>
              </select>

              <button
  onClick={submit}
  disabled={loading}
  className="w-full py-2 rounded-lg font-semibold shadow-lg"
>
  {loading ? "Predicting..." : "Predict Package"}
</button>

            </div>

            {result && (
              <div className="mt-6 p-4 rounded-xl" style={{ backgroundColor: "var(--bg-secondary)" }}>
                <p className="font-semibold">👤 Candidate: {form.name}</p>
                <p className="font-semibold">💰 Estimated Package: {result.predicted_package_lpa} LPA</p>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.75rem" }}>
                  Request ID: {result.request_id}
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </section>

      {/* ABOUT */}
      <section id="about" className="py-24">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h3 className="text-3xl font-bold mb-4">About This Project</h3>
          <p style={{ color: "var(--text-secondary)" }}>
            This is a full-stack ML engineering project demonstrating real-world
            model training, deployment, and UI integration. Built to showcase
            production-ready ML systems.
          </p>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t py-6 text-center text-sm" style={{ backgroundColor: "var(--bg-secondary)", color: "var(--text-secondary)" }}>
        © {new Date().getFullYear()} Package Predictor · Built with ML & FastAPI
      </footer>
    </div>
  );
}
