import React from "react";

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="flex items-center justify-between mt-4">

      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded disabled:opacity-50"
      >
        Prev
      </button>

      <span className="text-sm text-gray-600 dark:text-gray-300">
        Page {currentPage} of {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded disabled:opacity-50"
      >
        Next
      </button>

    </div>
  );
};

export default Pagination;
