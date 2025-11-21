import { User, Lock } from "lucide-react";

export const metadata = {
  title: "Login | My App",
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4">

      <h1 className="text-3xl font-semibold text-gray-800 mb-6">
        Welcome Back
      </h1>

      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-gray-200">

        <div className="flex items-center gap-3 border rounded-lg px-4 py-3 bg-gray-50 focus-within:border-blue-500 transition">
          <User className="text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Username"
            className="w-full bg-transparent outline-none text-gray-700"
          />
        </div>
        
        <div className="flex items-center gap-3 border rounded-lg px-4 py-3 bg-gray-50 mt-4 focus-within:border-blue-500 transition">
          <Lock className="text-gray-400" size={18} />
          <input
            type="password"
            placeholder="Password"
            className="w-full bg-transparent outline-none text-gray-700"
          />
        </div>

        <div className="flex justify-between items-center mt-4">
          <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
            <input type="checkbox" className="accent-blue-600" />
            Remember me
          </label>

          <button className="text-sm text-blue-600 hover:underline">
            Forgot Password?
          </button>
        </div>
        
        <button className="w-full mt-6 bg-green-500 hover:bg-green-700 text-white font-semibold py-2.5 rounded-lg shadow transition">
          LOGIN
        </button>

      </div>
    </div>
  );
}
