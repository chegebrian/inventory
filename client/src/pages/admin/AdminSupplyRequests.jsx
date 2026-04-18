import React, { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { toast } from "react-toastify";
import api from "../../utils/api";
import Table from "../../components/common/Table";
import EmptyState from "../../components/common/EmptyState";

const AdminSupplyRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const res = await api.get("/supply-requests/");
      setRequests(res.data.requests || []);
    } catch {
      toast.error("Failed to load supply requests");
    } finally {
      setLoading(false);
    }
  };

  const respond = async (id, status) => {
    if (!window.confirm(`Mark this request as ${status}?`)) return;

    try {
      await api.patch(`/supply-requests/${id}/respond`, { status });
      toast.success(`Request marked as ${status}`);
      fetchRequests();
    } catch {
      toast.error("Failed to update request");
    }
  };

  // =========================
  // 🎨 TABLE CONFIG
  // =========================
  const columns = [
    { header: "Product", accessor: "product_name" },
    { header: "Quantity", accessor: "quantity_requested" },
    { header: "Note", accessor: "note" },
    { header: "Status", accessor: "status" },
    { header: "Actions", accessor: "actions" },
  ];

  const tableData = requests.map((r) => ({
    product_name: (
      <span className="font-medium text-gray-800">
        {r.product_name}
      </span>
    ),

    quantity_requested: (
      <span className="text-gray-700">
        {r.quantity_requested}
      </span>
    ),

    note: (
      <span className="text-gray-500 text-sm">
        {r.note || "—"}
      </span>
    ),

    status: (
      <span
        className={
          r.status === "approved"
            ? "badge-approved"
            : r.status === "declined"
            ? "badge-declined"
            : "badge-pending"
        }
      >
        {r.status}
      </span>
    ),

    actions:
      r.status === "pending" ? (
        <div className="flex gap-2">
          <button
            onClick={() => respond(r.id, "approved")}
            className="btn-secondary text-xs px-3 py-1"
          >
            Approve
          </button>

          <button
            onClick={() => respond(r.id, "declined")}
            className="btn-danger text-xs px-3 py-1"
          >
            Reject
          </button>
        </div>
      ) : (
        <span className="text-gray-400 text-xs italic">
          Completed
        </span>
      ),
  }));

  return (
    <DashboardLayout title="Supply Requests">

      {/* 🔥 Header Section */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">
          Supply Requests
        </h1>
        <p className="text-gray-500 text-sm">
          Review and manage stock requests from clerks
        </p>
      </div>

      {/* 🔥 Card */}
      <div className="card hover:shadow-lg transition">

        {/* Table Header */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">
            All Requests
          </h2>

          <span className="text-sm text-gray-500">
            {requests.length} total
          </span>
        </div>

        {/* Content */}
        {loading ? (
          <div className="py-12 text-center text-gray-400">
            Loading requests...
          </div>
        ) : requests.length === 0 ? (
          <EmptyState
            title="No supply requests"
            message="All supply requests will appear here"
            icon="🚚"
          />
        ) : (
          <div className="overflow-x-auto">
            <Table columns={columns} data={tableData} />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AdminSupplyRequests;