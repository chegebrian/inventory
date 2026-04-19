import React, { useState, useEffect } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { toast } from "react-toastify";
import api from "../../utils/api";
import { useSelector, useDispatch } from "react-redux";
import { updateUser } from "../../store/slices/authSlice";

const EditProfile = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const [form, setForm] = useState({
    full_name: "",
    phone_number: "",
  });

  const [loading, setLoading] = useState(false);

  // Load current user data
  useEffect(() => {
    if (user) {
      setForm({
        full_name: user.full_name || "",
        phone_number: user.phone_number || "",
      });
    }
  }, [user]);

  // Submit handler
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // ✅ FIX: use PUT (matches backend)
      const res = await api.put("/auth/profile", form);

      // Update Redux (sidebar updates instantly)
      dispatch(updateUser(res.data.user));

      toast.success("Profile updated successfully");
    } catch (err) {
      console.error(err);
      toast.error(
        err.response?.data?.error || "Failed to update profile"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout title="Edit Profile 👤">
      <div className="card" style={{ maxWidth: "500px", margin: "0 auto" }}>
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>

          {/* Full Name */}
          <div>
            <label style={{ fontSize: "14px", fontWeight: "600" }}>
              Full Name
            </label>
            <input
              type="text"
              className="input-field"
              value={form.full_name}
              onChange={(e) =>
                setForm({ ...form, full_name: e.target.value })
              }
              required
            />
          </div>

          {/* Phone */}
          <div>
            <label style={{ fontSize: "14px", fontWeight: "600" }}>
              Phone Number
            </label>
            <input
              type="tel"
              className="input-field"
              value={form.phone_number}
              onChange={(e) =>
                setForm({ ...form, phone_number: e.target.value })
              }
            />
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: "100%" }}
          >
            {loading ? "Saving..." : "Save Changes"}
          </button>

        </form>
      </div>
    </DashboardLayout>
  );
};

export default EditProfile;