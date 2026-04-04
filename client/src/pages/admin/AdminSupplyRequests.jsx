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
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-4">Product</th>
                <th className="text-left py-4">Quantity</th>
                <th className="text-left py-4">Note</th>
                <th className="text-left py-4">Status</th>
                <th className="text-left py-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(r => (
                <tr key={r.id} className="border-b hover:bg-gray-50">
                  <td className="py-4 font-medium">{r.product_name}</td>
                  <td className="py-4">{r.quantity_requested}</td>
                  <td className="py-4 text-gray-600">{r.note || '—'}</td>
                  <td className="py-4">{r.status}</td>
                  <td className="py-4">Actions</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AdminSupplyRequests;