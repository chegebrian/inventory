import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css"; // ✅ MUST stay here

import { Provider } from "react-redux";
import { store } from "./store";

import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; // ✅ IMPORTANT

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />

      {/* Toast Notifications */}
      <ToastContainer
        position="top-right"
        autoClose={3000}
        newestOnTop
        closeOnClick
        pauseOnHover
        draggable
        theme="light"
      />
    </Provider>
  </React.StrictMode>
);