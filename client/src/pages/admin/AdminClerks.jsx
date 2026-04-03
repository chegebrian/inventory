import React, { useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';

const AdminClerks = () => {
  const [clerks, setClerks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [inviteEmail, setInviteEmail] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  return (
    <DashboardLayout title="Manage Clerks 👥">
      <div>Clerks</div>
    </DashboardLayout>
  );
};

export default AdminClerks;