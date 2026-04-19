import React from "react";
import Sidebar from "./Sidebar";

const DashboardLayout = ({ children, title }) => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* Sidebar */}
      <div style={{
        width: "260px",
        minWidth: "260px",
        background: "#111827",
        color: "white"
      }}>
        <Sidebar />
      </div>

      {/* Main */}
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden"
      }}>

        {/* Topbar */}
        <div style={{
          padding: "16px 20px",
          background: "white",
          borderBottom: "1px solid #e5e7eb",
          display: "flex",
          justifyContent: "space-between"
        }}>
          <h2>{title}</h2>
          <span>Admin Dashboard</span>
        </div>

        {/* Content */}
        <div style={{
          padding: "20px",
          overflowY: "auto",
          flex: 1
        }}>
          {children}
        </div>

      </div>
    </div>
  );
};

export default DashboardLayout;