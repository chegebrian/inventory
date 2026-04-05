import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div className="h-full w-64 bg-gray-900 text-white p-4">
      <h2 className="text-xl font-bold mb-6">LocalShop</h2>

      <ul className="space-y-3">
        <li>
          <Link to="/" className="hover:text-gray-300">Dashboard</Link>
        </li>
        <li>
          <Link to="/products" className="hover:text-gray-300">Products</Link>
        </li>
        <li>
          <Link to="/reports" className="hover:text-gray-300">Reports</Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;