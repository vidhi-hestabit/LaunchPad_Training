"use client";

import { LayoutDashboard, Folder, BarChart2, Table, ChevronRight } from "lucide-react";

export default function Sidebar({ isSidebarOpen }) {

  return (
    <aside
  className={`
    fixed top-16 left-0 h-[calc(100vh-4rem)]
    bg-gray-900 text-white shadow-lg
    overflow-hidden
    transition-all duration-300 z-40
    ${isSidebarOpen ? `w-56` : `w-0`}
  `}
>

      <div className="p-4 space-y-6 overflow-y-auto">
        <div>
          <h6 className="px-3 text-xs uppercase text-gray-500 mb-2">Core</h6>
          <SidebarLink icon={LayoutDashboard} label="Dashboard" active />
        </div>
        <div>
          <h6 className="px-3 text-xs uppercase text-gray-500 mb-2">Interface</h6>
          <DropdownLink icon={Folder} label="Layouts" />
          <DropdownLink icon={Folder} label="Pages" />
        </div>
        <div>
          <h6 className="px-3 text-xs uppercase text-gray-500 mb-2">Addons</h6>
          <SidebarLink icon={BarChart2} label="Charts" />
          <SidebarLink icon={Table} label="Tables" />
        </div>

      </div>
    </aside>
  );
}

function SidebarLink({ icon: Icon, label, active }) {
  return (
    <div className={`flex items-center p-3 rounded-md cursor-pointer 
      ${active ? "bg-gray-700" : "hover:bg-gray-700"}`}
    >
      <Icon size={18} className="mr-3" />
      <span className="text-sm">{label}</span>
    </div>
  );
}

function DropdownLink({ icon: Icon, label }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-md cursor-pointer hover:bg-gray-700 text-sm">
      <div className="flex items-center">
        <Icon size={18} className="mr-3" />
        {label}
      </div>
      <ChevronRight size={16} />
    </div>
  );
}
