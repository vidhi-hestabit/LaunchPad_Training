export default function Input({ label, className = "", ...props }) {
  return (
    <div className="flex flex-col space-y-1">
      {label && <label className="text-sm font-medium text-gray-600">{label}</label>}
      <input
        {...props}
        className={`px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 outline-none ${className}`}
      />
    </div>
  );
}