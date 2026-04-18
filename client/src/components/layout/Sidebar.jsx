import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../../store/slices/authSlice";
import { toast } from "react-toastify";

const Sidebar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    toast.success("Logged out successfully");
    setTimeout(() => {
      navigate("/", { replace: true });
    }, 100);
  };

  const merchantLinks = [
    { to: "/merchant/dashboard", icon: "📊", label: "Dashboard" },
    { to: "/merchant/stores", icon: "🏪", label: "Stores" },
    { to: "/merchant/admins", icon: "👔", label: "Admins" },
    { to: "/merchant/reports", icon: "📈", label: "Reports" },
  ];

  const adminLinks = [
    { to: "/admin/dashboard", icon: "📊", label: "Dashboard" },
    { to: "/admin/products", icon: "📦", label: "Products" },
    { to: "/admin/inventory", icon: "📋", label: "Inventory" },
    { to: "/admin/supply-requests", icon: "🚚", label: "Supply Requests" },
    { to: "/admin/clerks", icon: "📝", label: "Clerks" },
    { to: "/admin/reports", icon: "📈", label: "Reports" },
  ];

  const clerkLinks = [
    { to: "/clerk/dashboard", icon: "📊", label: "Dashboard" },
    { to: "/clerk/record-entry", icon: "📝", label: "Record Entry" },
    { to: "/clerk/my-entries", icon: "📋", label: "My Entries" },
    { to: "/clerk/supply-requests", icon: "🚚", label: "Supply Requests" },
  ];

  const commonLinks = [
    { to: "/profile/edit", icon: "👤", label: "Edit Profile" },
    { to: "/profile/change-password", icon: "🔑", label: "Change Password" },
  ];

  const links =
    user?.role === "merchant"
      ? merchantLinks
      : user?.role === "admin"
      ? adminLinks
      : clerkLinks;

  const linkStyle = {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "10px 16px",
    borderRadius: "8px",
    fontSize: "14px",
    textDecoration: "none",
    color: "#9ca3af",
    marginBottom: "4px",
  };

  return (
    <div
      style={{
        width: "260px",
        height: "100vh",
        background: "#111827",
        color: "white",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Logo */}
      <div
        style={{
          padding: "20px",
          borderBottom: "1px solid #1f2937",
          fontWeight: "bold",
          display: "flex",
          gap: "8px",
        }}
      >
        📦 LocalShop
      </div>

      {/* User */}
      <div
        style={{
          padding: "16px 20px",
          borderBottom: "1px solid #1f2937",
        }}
      >
        <div style={{ fontSize: "14px", fontWeight: "600" }}>
          {user?.full_name || "User"}
        </div>
        <div style={{ fontSize: "12px", color: "#9ca3af" }}>
          {user?.role || "guest"}
        </div>
      </div>

      {/* Links */}
      <div style={{ flex: 1, padding: "10px" }}>
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            style={({ isActive }) => ({
              ...linkStyle,
              background: isActive ? "#4f46e5" : "transparent",
              color: isActive ? "white" : "#9ca3af",
            })}
          >
            <span>{link.icon}</span>
            {link.label}
          </NavLink>
        ))}

        {/* Divider */}
        <div style={{ margin: "15px 0", borderTop: "1px solid #1f2937" }} />

        {commonLinks.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            style={({ isActive }) => ({
              ...linkStyle,
              background: isActive ? "#1f2937" : "transparent",
              color: isActive ? "white" : "#9ca3af",
            })}
          >
            <span>{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </div>

      {/* Logout */}
      <div style={{ padding: "16px", borderTop: "1px solid #1f2937" }}>
        <button
          onClick={handleLogout}
          style={{
            width: "100%",
            padding: "10px",
            background: "#ef4444",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          🚪 Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;