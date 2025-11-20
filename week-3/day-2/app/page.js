import { BarChart2, Table, ChevronRight } from "lucide-react";
import Card from "./components/ui/Card";
import Input from "./components/ui/Input";
import Button from "./components/ui/Button";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="w-full">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Dashboard</h1>
        <div className="w-full bg-gray-200 py-3 px-6">
          <p className="text-sm text-gray-600">Dashboard</p>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        <div className="bg-blue-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-blue-100 text-sm font-medium">Primary Card</div>

          <div className="text-sm mt-4 border-t border-blue-300/40 pt-4">
            <Button
              variant="primary"
              className="w-full flex justify-between items-center bg-transparent hover:bg-blue-700/40"
            >
              View Details <ChevronRight size={16} />
            </Button>
          </div>
        </div>

        <div className="bg-yellow-500 text-white rounded-lg p-6 shadow-lg">
          <div className="text-yellow-100 text-sm font-medium">Warning Card</div>

          <div className="text-sm mt-4 border-t border-yellow-300/40 pt-4">
            <Button
              variant="success"
              className="w-full flex justify-between items-center bg-transparent hover:bg-green-700/40"
            >
              View Details <ChevronRight size={16} />
            </Button>
          </div>
        </div>

        <div className="bg-green-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-green-100 text-sm font-medium">Success Card</div>

          <div className="text-sm mt-4 border-t border-green-300/40 pt-4">
            <Button
              variant="success"
              className="w-full flex justify-between items-center bg-transparent hover:bg-green-700/40"
            >
              View Details <ChevronRight size={16} />
            </Button>
          </div>
        </div>

        <div className="bg-red-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-red-100 text-sm font-medium">Danger Card</div>

          <div className="text-sm mt-4 border-t border-red-300/40 pt-4">
            <Button
              variant="danger"
              className="w-full flex justify-between items-center bg-transparent hover:bg-red-700/40"
            >
              View Details <ChevronRight size={16} />
            </Button>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

<Card>
  {/* Header */}
  <div className="flex items-center gap-2 mb-4">
    <BarChart2 size={18} color="black" />
    <h3 className="text-lg font-semibold text-black">Area Chart Example</h3>
  </div>

  {/* Chart */}
  <div className="bg-white rounded-lg p-6">
    <div className="flex">

      {/* Y-Axis Values */}
      <div className="flex flex-col justify-between h-64 mr-4 text-sm text-gray-600">
        {[40000, 30000, 20000, 10000, 0].map((val) => (
          <span key={val}>{val}</span>
        ))}
      </div>

      {/* Grid + Area Chart */}
      <div className="relative flex-1 h-64">

        {/* Horizontal Grid Lines */}
        <div className="absolute inset-0 flex flex-col justify-between">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="w-full border-t border-gray-200"></div>
          ))}
        </div>

        {/* SVG Area Line Chart */}
        <svg viewBox="0 0 600 200" className="absolute w-full h-full">
          <polyline
            fill="rgba(59, 130, 246, 0.25)"
            stroke="rgb(59, 130, 246)"
            strokeWidth="3"
            points="
              0,180
              50,150
              100,160
              150,120
              200,140
              250,90
              300,100
              350,60
              400,80
              450,40
              500,70
              550,30
              600,20 
              600,200 
              0,200
            "
          />

          {/* X-axis labels */}
          <text x="0" y="195" fontSize="12" fill="#666">Mar 1</text>
          <text x="250" y="195" fontSize="12" fill="#666">Mar 7</text>
          <text x="520" y="195" fontSize="12" fill="#666">Mar 13</text>
        </svg>
      </div>
    </div>
  </div>
</Card>


<Card>
  {/* Header */}
  <div className="flex items-center gap-2 mb-4">
    <BarChart2 size={18} color="black" />
    <h3 className="text-lg font-semibold text-black">Bar Chart Example</h3>
  </div>

  {/* Chart Container */}
  <div className="bg-white rounded-lg p-6">
    <div className="flex">

      {/* Y-Axis Values */}
      <div className="flex flex-col justify-between h-64 mr-4 text-sm text-gray-600">
        {[15000, 10000, 5000, 0].map((val) => (
          <span key={val}>{val}</span>
        ))}
      </div>

      {/* Grid + Bars */}
      <div className="relative flex-1">

        {/* Horizontal Grid Lines */}
        <div className="absolute inset-0 flex flex-col justify-between">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="w-full border-t border-gray-200"></div>
          ))}
        </div>

        {/* Bars */}
        <div className="absolute bottom-0 left-0 right-0 flex justify-around items-end h-64 px-4">
          {[4000, 5000, 6000, 8000, 10000, 15000].map((val, i) => (
            <div key={i} className="flex flex-col items-center h-full justify-end">

              <div
                className="bg-blue-600 w-[70px] rounded-t"
                style={{ height: `${(val / 15000) * 100}%` }}
              ></div>

              <span className="text-xs text-gray-700 mt-2">
                {["Jan", "Feb", "Mar", "Apr", "May", "Jun"][i]}
              </span>
            </div>
          ))}
        </div>

      </div>
    </div>
  </div>
</Card>


      </div>

      {/* Data Table */}
      <Card>
        <div className="flex items-center gap-2 mb-4 text-black">
          <Table size={18} />
          <h3 className="text-black font-semibold">Datatable Example</h3>
        </div>

        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Show</span>
            <select className="border border-gray-300 rounded px-2 py-1 text-black">
              <option>10</option>
              <option>25</option>
              <option>50</option>
            </select>
            <span className="text-sm text-gray-600">entries</span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Search:</span>
            <Input placeholder="" className="w-48" />
          </div>
        </div>

        <div className="text-sm text-gray-600 text-center py-8 border-t border-b">
          Sample data table content
        </div>
      </Card>
    </div>
  );
}
