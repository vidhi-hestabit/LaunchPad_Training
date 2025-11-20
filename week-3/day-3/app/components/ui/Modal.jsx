"use client";

import { useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function Modal({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex min-h-screen bg-gray-100">
      <Navbar toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <Sidebar isSidebarOpen={sidebarOpen} />
      <main
        className={`pt-20 p-6 w-full transition-all duration-300 ${
          sidebarOpen ? "lg:ml-56" : "lg:ml-20"
        }`}
      >
        {children}
      </main>
    </div>
  );
}