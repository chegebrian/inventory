import React from 'react';

const LoadingSpinner = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-12 h-12 border-4 border-gray-800 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-500 mt-4 text-sm">{message}</p>
    </div>
  );
};

export default LoadingSpinner;