import React, { useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';

const AdminSupplyRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  return (
    <DashboardLayout title="Supply Requests 🚚">
      <div>Supply Requests</div>
    </DashboardLayout>
  );
};

export default AdminSupplyRequests;