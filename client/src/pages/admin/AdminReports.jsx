import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { toast } from 'react-toastify';
import api from '../../utils/api';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts';

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

  const exportToPDF = async () => {
    setExporting(true);
    try {
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();

      pdf.setFontSize(18);
      pdf.text("Inventory App", pageWidth / 2, 20, { align: 'center' });

      const chartElement = document.getElementById('report-charts');
      if (chartElement) {
        const canvas = await html2canvas(chartElement, { scale: 2 });
        const imgData = canvas.toDataURL('image/png');
        pdf.addImage(imgData, 'PNG', 20, 120, 170, 95);
      }

      pdf.save(`Admin_Report_${new Date().toISOString().slice(0,10)}.pdf`);
      toast.success('Report exported to PDF');
    } catch {
      toast.error('Failed to generate PDF');
    } finally {
      setExporting(false);
    }
  };

  return (
    <DashboardLayout title="Reports 📈">
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div>
            <input type="date" className="input-field" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>
          <div>
            <input type="date" className="input-field" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </div>
          <button onClick={exportToPDF} disabled={exporting} className="btn-primary h-10 mt-6">
            {exporting ? 'Exporting...' : 'Export to PDF'}
          </button>
        </div>
      </div>

      <div id="report-charts" className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Store Performance</h3>
          <ResponsiveContainer width="100%" height={420}>
            <BarChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="quantity_received" />
              <Bar dataKey="quantity_in_stock" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Trend Over Time</h3>
          <ResponsiveContainer width="100%" height={420}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="product_name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="quantity_received" />
              <Line type="monotone" dataKey="quantity_in_stock" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default AdminReports;