import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';
import StatCard from '../../components/common/StatCard';

const ClerkDashboard = () => {
  const [summary, setSummary] = useState({});
  const [recentEntries, setRecentEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchSummary(), fetchRecentEntries()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const fetchSummary = async () => {
    try {
      const res = await api.get('/inventory/report/summary');
      setSummary(res.data.summary || {});
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to load summary');
    }
  };

  const fetchRecentEntries = async () => {
    try {
      const res = await api.get('/inventory/my-entries?limit=6');
      setRecentEntries(res.data.entries || []);
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to load recent entries');
    }
  };

  if (loading) {
    return <DashboardLayout title="Clerk Dashboard 📋"><div className="text-center py-20">Loading dashboard...</div></DashboardLayout>;
  }

  return (
    <DashboardLayout title="Clerk Dashboard 📋">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Received" value={summary.total_items_received || 0} icon="📥" color="bg-blue-500" />
        <StatCard title="Items In Stock" value={summary.total_items_in_stock || 0} icon="📦" color="bg-green-500" />
        <StatCard title="Spoilt Items" value={summary.total_items_spoilt || 0} icon="⚠️" color="bg-red-500" />
        <StatCard title="Unpaid Amount" value={`KES ${(summary.total_unpaid_amount || 0).toLocaleString()}`} icon="💰" color="bg-orange-500" />
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Recent Entries</h3>
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700">
              <th className="text-left py-4">Product</th>
              <th className="text-left py-4">Quantity</th>
              <th className="text-left py-4">Payment Status</th>
            </tr>
          </thead>
          <tbody>
            {recentEntries.map(entry => (
              <tr key={entry.id} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="py-4 font-medium text-gray-800 dark:text-white">{entry.product_name}</td>
                <td className="py-4">{entry.quantity_received}</td>
                <td className="py-4">
                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                    entry.payment_status === 'paid' 
                      ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300' 
                      : 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300'
                  }`}>
                    {entry.payment_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DashboardLayout>
  );
};

export default ClerkDashboard;
