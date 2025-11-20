"use client";
import { useState } from "react";
import "./globals.css";
import Navbar from "./components/ui/Navbar";
import Sidebar from "./components/ui/Sidebar";

export default function RootLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <html lang="en">
      <body className="flex">
        <Sidebar isSidebarOpen={isSidebarOpen} />
        <div className="flex-1 flex flex-col">
        <Navbar toggleSidebar={toggleSidebar} />
          <main className="p-6 bg-gray-100 min-h-screen">
            {children}
          </main>

        </div>
      </body>
    </html>
  );
}
