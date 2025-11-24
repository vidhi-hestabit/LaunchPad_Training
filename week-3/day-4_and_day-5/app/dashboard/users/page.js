"use client";

import { Search, Shield } from "lucide-react";
import { useState } from "react";

export default function Users() {
  const [search, setSearch] = useState("");

  const users = [
    { name: "User", email: "user@example.com", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "Dr. Ray Stoltenberg", email: "rosalinda42@example.com", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "Mrs. Mertie Murray MD", email: "ernser.susanna@example.net", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "User", email: "user@example.com", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "Dr. Ray Stoltenberg", email: "rosalinda42@example.com", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "Mrs. Mertie Murray MD", email: "ernser.susanna@example.net", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
    { name: "User", email: "user@example.com", role: "User", createdAt: "18/10/2024 05:27", updatedAt: "18/10/2024 05:27" },
  ];

  const filtered = users.filter((u) => {
    const s = search.toLowerCase();
    return u.name.toLowerCase().includes(s) || u.email.toLowerCase().includes(s);
  });

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="text-sm text-gray-500 mb-2">Users &gt; List</div>
      <h1 className="text-3xl font-semibold text-gray-800 mb-6">Users</h1>

      <div className="bg-white rounded-xl shadow-sm p-6 border">
        <div className="flex justify-end mb-4 relative">
          <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
          <input
            type="text"
            placeholder="Search"
            className="border rounded-lg pl-10 pr-4 py-2 text-sm w-64 focus:ring-2 focus:ring-blue-500"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <table className="w-full border-collapse">
          <thead>
            <tr className="text-left text-gray-500 text-sm border-b">
              {['Name ↓','Email ↓','Role ↓','Created at','Updated at','Action'].map((h) => (
                <th key={h} className="py-3 px-3 {h === 'Action' ? 'text-right' : ''}">{h}</th>
              ))}
            </tr>
          </thead>

          <tbody>
            {filtered.map((user, i) => (
              <tr key={i} className="border-b hover:bg-gray-50 text-black">
                <td className="py-4 px-3">{user.name}</td>
                <td className="py-4 px-3">{user.email}</td>
                <td className="py-4 px-3">{user.role}</td>
                <td className="py-4 px-3">{user.createdAt}</td>
                <td className="py-4 px-3">{user.updatedAt}</td>
                <td className="py-4 px-3 text-right"><Shield size={20} className="text-purple-500 cursor-pointer" /></td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="flex justify-between items-center mt-4 text-sm text-gray-600">
          <span>Showing 1 to 10 of 12 results</span>
          <div className="flex items-center gap-2">
            <select className="border rounded-md px-2 py-1 cursor-pointer">
              {[10, 20, 50].map((n) => <option key={n}>{n}</option>)}
            </select>
            <div className="flex items-center gap-1">
              {["<", "1", "2", ">"].map((p, idx) => (
                <button key={idx} className={`border rounded-md px-3 py-1 ${p === "1" ? "bg-gray-200 font-semibold" : "hover:bg-gray-100"}`}>{p}</button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}