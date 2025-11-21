import { BarChart2, Table, ChevronRight, AreaChart } from "lucide-react";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Dashboard</h1>
      <div className="w-full bg-gray-200 py-3 px-6">
        <p className="text-sm text-gray-600">Dashboard</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-blue-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-blue-100 text-sm font-medium">Primary Card</div>
          <div className="text-sm mt-4 border-t border-blue-300/40 pt-4">
            <Button variant="primary">View Details</Button>
          </div>
        </div>

        <div className="bg-yellow-500 text-white rounded-lg p-6 shadow-lg">
          <div className="text-yellow-100 text-sm font-medium">
            Warning Card
          </div>
          <div className="text-sm mt-4 border-t border-yellow-300/40 pt-4">
            <Button variant="warning">View Details</Button>
          </div>
        </div>

        <div className="bg-green-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-green-100 text-sm font-medium">Success Card</div>
          <div className="text-sm mt-4 border-t border-green-300/40 pt-4">
            <Button variant="success">View Details</Button>
          </div>
        </div>

        <div className="bg-red-600 text-white rounded-lg p-6 shadow-lg">
          <div className="text-red-100 text-sm font-medium">Danger Card</div>
          <div className="text-sm mt-4 border-t border-red-300/40 pt-4">
            <Button variant="danger">View Details</Button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Area Chart Example">
          <div className="flex items-center gap-2 mb-4">
            <AreaChart size={18} />
            <span className="text-sm text-gray-600">Area Chart Example</span>
          </div>
          <div className="flex">
            <div className="flex flex-col justify-between h-64 mr-4 text-sm text-gray-600">
              {[40000, 30000, 20000, 10000, 0].map((v) => (
                <span key={v}>{v}</span>
              ))}
            </div>
            <div className="relative flex-1 h-64">
              <div className="absolute inset-0 flex flex-col justify-between">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="w-full border-t border-gray-200"
                  ></div>
                ))}
              </div>
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
                <text x="0" y="195" fontSize="12" fill="#666">
                  Mar 1
                </text>
                <text x="250" y="195" fontSize="12" fill="#666">
                  Mar 7
                </text>
                <text x="520" y="195" fontSize="12" fill="#666">
                  Mar 13
                </text>
              </svg>
            </div>
          </div>
        </Card>

        <Card title="Bar Chart Example">
          <div className="flex items-center gap-2 mb-4">
            <BarChart2 size={18} color="black" />
            <h3 className="text-lg font-semibold text-black">
              Bar Chart Example
            </h3>
          </div>
          <div className="flex">
            <div className="flex flex-col justify-between h-64 mr-4 text-sm text-gray-600">
              {[15000, 10000, 5000, 0].map((val) => (
                <span key={val}>{val}</span>
              ))}
            </div>
            <div className="relative flex-1">
              <div className="absolute inset-0 flex flex-col justify-between">
                {[...Array(4)].map((_, i) => (
                  <div
                    key={i}
                    className="w-full border-t border-gray-200"
                  ></div>
                ))}
              </div>
              <div className="absolute bottom-0 left-0 right-0 flex justify-around items-end h-64 px-4">
                {[4000, 5000, 6000, 8000, 10000, 15000].map((val, i) => (
                  <div
                    key={i}
                    className="flex flex-col items-center h-full justify-end"
                  >
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
        </Card>
      </div>
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
      </Card>
    </div>
  );
}
