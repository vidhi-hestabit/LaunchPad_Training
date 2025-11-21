import { UserCircle } from "lucide-react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";

export default function ProfilePage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Profile</h1>
        <div className="text-sm text-gray-500">Dashboard / Profile</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="User Information">
          <div className="flex flex-col items-center">
            <div className="w-24 h-24 bg-gray-300 rounded-full flex items-center justify-center mb-4">
              <UserCircle size={48} className="text-gray-600" />
            </div>
            <h3 className="text-xl font-semibold mb-1 text-black">Nina Valentine</h3>
            <Button variant="success">Active</Button>
            <p className="text-sm text-gray-600 mt-4 text-center">
              Web Developer & Designer
            </p>
          </div>
        </Card>

        <div className="lg:col-span-2 space-y-6">
          <Card title="Profile Details">
            <div className="space-y-4">
              <Input label="Full Name" defaultValue="Nina Valentine" />
              <Input label="Email" type="email" defaultValue="nina.valentine@example.com" />
              <Input label="Phone" defaultValue="+1 234 567 8900" />
              <div className="flex gap-2">
                <Button variant="primary">Save Changes</Button>
                <Button variant="outline">Cancel</Button>
              </div>
            </div>
          </Card>

          <Card title="Account Settings">
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="text-sm text-black">Email Notifications</span>
                <input type="checkbox" className="w-4 h-4" defaultChecked />
              </div>
              <div className="text-black flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="text-sm">Two-Factor Authentication</span>
                <input type="checkbox" className="w-4 h-4" />
              </div>
              <div className="text-black flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="text-sm">Monthly Reports</span>
                <input type="checkbox" className="w-4 h-4" defaultChecked />
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}