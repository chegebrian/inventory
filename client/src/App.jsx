import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DashboardLayout from "./components/layout/DashboardLayout";

function App() {
  return (
    <Router>
      <Routes>

        <Route
          path="/"
          element={
            <DashboardLayout title="Dashboard">
              <h2 className="text-xl">Welcome 👋</h2>
              <p>Your layout is working perfectly.</p>
            </DashboardLayout>
          }
        />

      </Routes>
    </Router>
  );
}

export default App;