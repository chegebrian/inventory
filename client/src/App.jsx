import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DashboardLayout from "./components/layout/DashboardLayout";

import LoadingSpinner from "./components/common/LoadingSpinner";
import EmptyState from "./components/common/EmptyState";

function App() {
  return (
    <Router>
      <Routes>

        {/* Dashboard */}
        <Route
          path="/"
          element={
            <DashboardLayout title="Dashboard">

              <h2 className="text-xl font-semibold mb-4">
                Component Test
              </h2>

              {/* Loading Spinner */}
              <LoadingSpinner message="Fetching data..." />

              {/* Empty State */}
              <EmptyState 
                title="No Products Yet"
                message="Start by adding your first product"
                icon="📦"
              />

            </DashboardLayout>
          }
        />

        {/* Products */}
        <Route
          path="/products"
          element={
            <DashboardLayout title="Products">
              <h2 className="text-xl font-semibold">Products Page</h2>
              <p className="text-gray-600 mt-2">
                Manage your products here.
              </p>
            </DashboardLayout>
          }
        />

        {/* Reports */}
        <Route
          path="/reports"
          element={
            <DashboardLayout title="Reports">
              <h2 className="text-xl font-semibold">Reports Page</h2>
              <p className="text-gray-600 mt-2">
                View analytics and reports here.
              </p>
            </DashboardLayout>
          }
        />

        {/* Fallback */}
        <Route
          path="*"
          element={
            <DashboardLayout title="Not Found">
              <h2 className="text-xl font-semibold">
                404 - Page Not Found
              </h2>
            </DashboardLayout>
          }
        />

      </Routes>
    </Router>
  );
}

export default App;
