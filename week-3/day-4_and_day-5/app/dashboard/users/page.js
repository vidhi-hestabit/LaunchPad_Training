"use client";

import { Search, Shield } from "lucide-react";
import { useState } from "react";

export default function Users() {
  const [search, setSearch] = useState("");

  const users = [
    {
      name: "User",
      email: "user@example.com",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },
    {
      name: "Dr. Ray Stoltenberg",
      email: "rosalinda42@example.com",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },
    {
      name: "Mrs. Mertie Murray MD",
      email: "ernser.susanna@example.net",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },{
      name: "User",
      email: "user@example.com",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },
    {
      name: "Dr. Ray Stoltenberg",
      email: "rosalinda42@example.com",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },
    {
      name: "Mrs. Mertie Murray MD",
      email: "ernser.susanna@example.net",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },{
      name: "User",
      email: "user@example.com",
      role: "User",
      createdAt: "18/10/2024 05:27",
      updatedAt: "18/10/2024 05:27",
    },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Breadcrumb */}
      <div className="text-sm text-gray-500 mb-2">Users &gt; List</div>

      {/* Title */}
      <h1 className="text-3xl font-semibold text-gray-800 mb-6">Users</h1>

      {/* Table Container */}
      <div className="bg-white rounded-xl shadow-sm p-6 border">
        
        {/* Top Bar: Search */}
        <div className="flex justify-end mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
            <input
              type="text"
              placeholder="Search"
              className="border rounded-lg pl-10 pr-4 py-2 text-sm w-64 focus:ring-2 focus:ring-blue-500 outline-none"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {/* Table */}
        <table className="w-full border-collapse">
          <thead>
            <tr className="text-left text-gray-500 text-sm border-b">
              <th className="py-3 px-3">Name ↓</th>
              <th className="py-3 px-3">Email ↓</th>
              <th className="py-3 px-3">Role ↓</th>
              <th className="py-3 px-3">Created at</th>
              <th className="py-3 px-3">Updated at</th>
              <th className="py-3 px-3 text-right">Action</th>
            </tr>
          </thead>

          <tbody>
            {users.map((user, index) => (
              <tr key={index} className="border-b hover:bg-gray-50 text-black">
                <td className="py-4 px-3">{user.name}</td>
                <td className="py-4 px-3">{user.email}</td>
                <td className="py-4 px-3">{user.role}</td>
                <td className="py-4 px-3">{user.createdAt}</td>
                <td className="py-4 px-3">{user.updatedAt}</td>
                <td className="py-4 px-3 text-right">
                  <Shield size={20} className="text-purple-500 cursor-pointer" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Footer + Pagination */}
        <div className="flex justify-between items-center mt-4 text-sm text-gray-600">
          <div>Showing 1 to 10 of 12 results</div>

          <div className="flex items-center gap-2">
            {/* Per page dropdown */}
            <select className="border rounded-md px-2 py-1 cursor-pointer">
              <option>10</option>
              <option>20</option>
              <option>50</option>
            </select>

            {/* Pagination */}
            <div className="flex items-center gap-1">
              <button className="border rounded-md px-3 py-1 hover:bg-gray-100">&lt;</button>
              <button className="border rounded-md px-3 py-1 bg-gray-200 font-semibold">1</button>
              <button className="border rounded-md px-3 py-1 hover:bg-gray-100">2</button>
              <button className="border rounded-md px-3 py-1 hover:bg-gray-100">&gt;</button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
