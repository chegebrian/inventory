import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { useSelector } from 'react-redux';
import { toast } from 'react-toastify';
import api from '../../utils/api';

const AdminClerks = () => {
  const [clerks, setClerks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [inviteEmail, setInviteEmail] = useState('');
  const [deletingId, setDeletingId] = useState(null);
  const { user } = useSelector(state => state.auth);

  const fetchClerks = async () => {
    setLoading(true);
    try {
      const res = await api.get('/auth/users?role=clerk');
      setClerks(res.data.users || []);
    } catch {
      toast.error('Failed to load clerks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClerks();
  }, []);

  return (
    <DashboardLayout title="Manage Clerks 👥">
      <div>Clerks</div>
    </DashboardLayout>
  );
};

export default AdminClerks;