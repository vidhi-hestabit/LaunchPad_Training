"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { 
  LayoutDashboard, 
  Folder, 
  BarChart2, 
  Table, 
  ChevronRight,
  Home,
  Info,
  UserCircle
} from "lucide-react";

export default function Sidebar({ isSidebarOpen }) {
  const pathname = usePathname();

  return (
    <aside
      className={`fixed top-16 left-0 h-[calc(100vh-4rem)] bg-gray-900 text-white shadow-lg transition-all duration-300 z-40 overflow-y-auto ${
        isSidebarOpen ? "w-56" : "w-0"
      }`}
    >
      <div className="p-4 space-y-6">
<div>
  <h6 className={`px-3 text-xs uppercase text-gray-500 mb-2 ${!isSidebarOpen && "hidden"}`}>
    CORE
  </h6>

  <SidebarLink
    href="/dashboard"
    icon={LayoutDashboard}
    label="Dashboard"
    active={pathname === "/dashboard"}
    isOpen={isSidebarOpen}
  />

  <SidebarLink
    href="/dashboard/users"
    icon={UserCircle}
    label="Users"
    active={pathname === "/dashboard/users.js"}
    isOpen={isSidebarOpen}
  />
</div>

        <div>
          <h6 className={`px-3 text-xs uppercase text-gray-500 mb-2 ${!isSidebarOpen && "hidden"}`}>
            INTERFACE
          </h6>
          <DropdownLink icon={Folder} label="Layouts" isOpen={isSidebarOpen} />
          <DropdownLink icon={Folder} label="Pages" isOpen={isSidebarOpen} />
        </div>


        <div>
          <h6 className={`px-3 text-xs uppercase text-gray-500 mb-2 ${!isSidebarOpen && "hidden"}`}>
            ADDONS
          </h6>
          <SidebarLink
            href="#"
            icon={BarChart2}
            label="Charts"
            isOpen={isSidebarOpen}
          />
          <SidebarLink
            href="#"
            icon={Table}
            label="Tables"
            isOpen={isSidebarOpen}
          />
        </div>


        <div>
          <h6 className={`px-3 text-xs uppercase text-gray-500 mb-2 ${!isSidebarOpen && "hidden"}`}>
            PAGES
          </h6>
          <SidebarLink
            href="/"
            icon={Home}
            label="Home"
            active={pathname === "/"}
            isOpen={isSidebarOpen}
          />
          <SidebarLink
            href="/about"
            icon={Info}
            label="About"
            active={pathname === "/about"}
            isOpen={isSidebarOpen}
          />
          <SidebarLink
            href="/profile"
            icon={UserCircle}
            label="Profile"
            active={pathname === "/profile"}
            isOpen={isSidebarOpen}
          />

        </div>
      </div>
    </aside>
  );
}

function SidebarLink({ href, icon: Icon, label, active, isOpen }) {
  return (
    <Link
      href={href}
      className={`flex items-center p-3 rounded-md cursor-pointer ${
        active ? "bg-gray-700" : "hover:bg-gray-700"
      }`}
    >
      <Icon size={18} className={isOpen ? "mr-3" : "mx-auto"} />
      {isOpen && <span className="text-sm">{label}</span>}
    </Link>
  );
}

function DropdownLink({ icon: Icon, label, isOpen }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-md cursor-pointer hover:bg-gray-700 text-sm">
      <div className="flex items-center">
        <Icon size={18} className={isOpen ? "mr-3" : "mx-auto"} />
        {isOpen && label}
      </div>
      {isOpen && <ChevronRight size={16} />}
    </div>
  );
}