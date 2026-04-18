import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { loginUser } from "../../store/slices/authSlice";
import { toast } from "react-toastify";

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading } = useSelector((state) => state.auth);

  const { register, handleSubmit } = useForm();
  const [showPassword, setShowPassword] = useState(false);

  const onSubmit = async (data) => {
    const res = await dispatch(loginUser(data));

    if (res.meta.requestStatus === "fulfilled") {
      toast.success("Login successful");

      const role = res.payload.user.role;
      if (role === "merchant") navigate("/merchant/dashboard");
      else if (role === "admin") navigate("/admin/dashboard");
      else navigate("/clerk/dashboard");
    } else {
      toast.error(res.payload || "Login failed");
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        {/* Header */}
        <div style={styles.header}>
          <h1 style={styles.logo}>📦 LocalShop</h1>
          <p style={styles.subtitle}>Welcome back 👋</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} style={styles.form}>

          {/* Email */}
          <div>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              {...register("email")}
              style={styles.input}
              required
            />
          </div>

          {/* Password */}
          <div style={{ position: "relative" }}>
            <label style={styles.label}>Password</label>
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password"
              {...register("password")}
              style={styles.input}
              required
            />

            <span
              onClick={() => setShowPassword(!showPassword)}
              style={styles.eye}
            >
              {showPassword ? "🙈" : "👁"}
            </span>
          </div>

          {/* Forgot Password */}
          <div style={styles.forgotWrapper}>
            <Link to="/forgot-password" style={styles.link}>
              Forgot password?
            </Link>
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.button,
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

        {/* Register */}
        <p style={styles.registerText}>
          Don’t have an account?{" "}
          <Link to="/register" style={styles.linkStrong}>
            Create one
          </Link>
        </p>

        {/* Footer */}
        <p style={styles.footer}>© 2026 LocalShop</p>

      </div>
    </div>
  );
};

export default Login;

/* =========================
   STYLES
========================= */
const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #eef2ff, #f9fafb)",
  },
  card: {
    width: "100%",
    maxWidth: "400px",
    background: "#fff",
    padding: "32px",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
  },
  header: {
    textAlign: "center",
    marginBottom: "24px",
  },
  logo: {
    margin: 0,
    fontSize: "26px",
    fontWeight: "700",
  },
  subtitle: {
    marginTop: "6px",
    fontSize: "14px",
    color: "#6b7280",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "18px",
  },
  label: {
    fontSize: "13px",
    fontWeight: "600",
    marginBottom: "4px",
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    border: "1px solid #d1d5db",
  },
  eye: {
    position: "absolute",
    right: "12px",
    top: "38px",
    cursor: "pointer",
  },
  forgotWrapper: {
    textAlign: "right",
    marginTop: "-10px",
  },
  link: {
    fontSize: "13px",
    color: "#6366f1",
    textDecoration: "none",
  },
  linkStrong: {
    color: "#4f46e5",
    fontWeight: "600",
    textDecoration: "none",
  },
  button: {
    marginTop: "10px",
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    background: "linear-gradient(135deg, #4f46e5, #6366f1)",
    color: "white",
    fontWeight: "600",
  },
  registerText: {
    marginTop: "16px",
    textAlign: "center",
    fontSize: "13px",
  },
  footer: {
    marginTop: "20px",
    textAlign: "center",
    fontSize: "12px",
    color: "#9ca3af",
  },
};