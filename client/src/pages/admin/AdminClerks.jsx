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

  const sendInvite = async (e) => {
    e.preventDefault();
    if (!inviteEmail) return toast.error('Email is required');

    try {
      await api.post('/auth/invite', {
        email: inviteEmail,
        role: 'clerk',
        store_id: user?.store_id
      });
      toast.success(`Invite sent to ${inviteEmail}`);
      setInviteEmail('');
      fetchClerks();
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to send invite');
    }
  };

  useEffect(() => {
    fetchClerks();
  }, []);

  return (
    <DashboardLayout title="Manage Clerks 👥">
      <div className="card">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">All Clerks</h2>

          <form onSubmit={sendInvite} className="flex gap-3">
            <input
              type="email"
              placeholder="Clerk email"
              className="input-field w-72"
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary">Send Invite</button>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AdminClerks;