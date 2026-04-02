import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';

const AdminInventory = () => {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  
  return <div>Admin Inventory</div>;

  return (
    <DashboardLayout title="Inventory Entries 📋">
        <div>Admin Inventory</div>
    </DashboardLayout>
    );

};



export default AdminInventory;