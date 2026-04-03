import React, { useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';

const AdminReports = () => {
  const [summary, setSummary] = useState({});
  const [trendData, setTrendData] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [exporting, setExporting] = useState(false);

  return (
    <DashboardLayout title="Reports 📈">
      <div>Reports</div>
    </DashboardLayout>
  );
};

export default AdminReports;