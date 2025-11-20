import Button from "../components/ui/Button";
import Card from "../components/ui/Card";

export default function AboutPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">About</h1>
      
      <Card title="About This Project">
        <p className="text-gray-600 mb-4">
          This is a demonstration of Next.js 13+ App Router with routing and layout system.
        </p>
        
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-800 mb-2">Server Components vs Client Components</h4>
            <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm text-black">
              <p>
                <strong>Server Components:</strong> Default in Next.js App Router. Rendered on server, 
                no JavaScript sent to client, can access backend resources directly.
              </p>
              <p>
                <strong>Client Components:</strong> Use "use client" directive. Enable interactivity 
                with useState, useEffect, event handlers. Rendered on client side.
              </p>
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 mb-2">Routing Structure</h4>
            <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm text-gray-700">
              <div>app/</div>
              <div className="pl-4">├── page.js (Home - /)</div>
              <div className="pl-4">├── about/</div>
              <div className="pl-8">└── page.js (About - /about)</div>
              <div className="pl-8">└── profile/</div>
              <div className="pl-12">└── page.js (Profile - /profile)</div>
              <div className="pl-4">└── layout.js (Root Layout)</div>
            </div>
          </div>
        </div>
      </Card>

      <Card title="Technology Stack">
        <div className="flex flex-wrap gap-2">
          <Button variant="primary">Next.js 13+</Button>
          <Button variant="success">React</Button>
          <Button variant="warning">Tailwind CSS</Button>
          <Button variant="danger">Lucide Icons</Button>
        </div>
      </Card>
    </div>
  );
}