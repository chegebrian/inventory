import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';

const AdminReports = () => {
  const [summary, setSummary] = useState({});
  const [trendData, setTrendData] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [exporting, setExporting] = useState(false);

  const fetchReports = async () => {
    try {
      let url = '/inventory/report/summary';
      if (startDate) url += `?start_date=${startDate}`;
      if (endDate) url += `&end_date=${endDate}`;

      const res = await api.get(url);
      setSummary(res.data.summary || {});

      const trendRes = await api.get('/inventory/report/trend');
      setTrendData(trendRes.data.trend || []);
    } catch {
      toast.error('Failed to load reports');
    }
  };

  useEffect(() => {
    fetchReports();
  }, [startDate, endDate]);

  return (
    <DashboardLayout title="Reports 📈">
      <div>Reports</div>
    </DashboardLayout>
  );
};

export default AdminReports;