import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import api from '../../utils/api';
import { toast } from 'react-toastify';

const AdminInventory = () => {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  fetchEntries();
  }, []);

  const fetchEntries = async () => {
    setLoading(true);
    try {
      const res = await api.get('/inventory/');
      setEntries(res.data.entries || []);
    } catch {
      toast.error('Failed to load inventory entries');
    } finally {
      setLoading(false);
    }
  };


  return <div>Admin Inventory</div>;

  return (
    <DashboardLayout title="Inventory Entries 📋">
        <div>Admin Inventory</div>
    </DashboardLayout>
    );

};



export default AdminInventory;