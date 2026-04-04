import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';

const AdminSupplyRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRequests = async () => {
    setLoading(true);
    try {
      const res = await api.get('/supply-requests/');
      setRequests(res.data.requests || []);
    } catch {
      toast.error('Failed to load supply requests');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  return (
    <DashboardLayout title="Supply Requests 🚚">
      <div className="card">
        <h2 className="text-xl font-semibold mb-6">Supply Requests</h2>

        {loading ? (
          <p className="text-center py-10 text-gray-400">
            Loading requests...
          </p>
        ) : (
          <div>Table coming soon</div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AdminSupplyRequests;