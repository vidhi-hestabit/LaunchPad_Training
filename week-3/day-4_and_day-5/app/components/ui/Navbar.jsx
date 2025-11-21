import { Menu, Search, User } from "lucide-react";
import Link from "next/link";

export default function Navbar({ toggleSidebar }) {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-gray-800 text-white h-16 shadow-md flex justify-between items-center px-4">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-semibold">Start Bootstrap</h1>
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-md hover:bg-gray-700"
        >
          <Menu size={20} />
        </button>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-stretch border border-gray-700">
          <input
            type="text"
            placeholder="Search for..."
            className="bg-white px-4 py-2 text-sm outline-none placeholder:text-black text-black"
          />
          <button
            type="submit"
            className="bg-blue-600 px-4 flex items-center justify-center"
          >
            <Search size={15} className="text-white" />
          </button>
        </div>

        <Link href="/login">
          <button className="p-2 hover:bg-gray-800 flex items-center gap-2 cursor-pointer">
            <User size={20} />
          </button>
        </Link>
      </div>
    </nav>
  );
}
