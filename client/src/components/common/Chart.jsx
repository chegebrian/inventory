import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Jan", sales: 400 },
  { name: "Feb", sales: 300 },
  { name: "Mar", sales: 500 },
  { name: "Apr", sales: 200 },
];

const Chart = () => {
  return (
    <div className="bg-white dark:bg-gray-900 p-4 rounded-2xl shadow">
      <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
        Sales Overview
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="sales" stroke="#6366f1" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Chart;