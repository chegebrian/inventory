import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const AdminDashboard = () => {
  const [summary, setSummary] = useState({});
  const [trendData, setTrendData] = useState([]);

  // fetch dashboard data from backend
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [summaryRes, trendRes] = await Promise.all([
          api.get('/inventory/report/summary'),
          api.get('/inventory/report/trend')
        ]);
        setSummary(summaryRes.data.summary || {});
        setTrendData(trendRes.data.trend || []);
      } catch (err) {
        toast.error('Failed to load dashboard data');
      }
    };
    fetchDashboardData();
  }, []);

  return (
    <DashboardLayout title="Admin Dashboard 📊">

      
    </DashboardLayout>