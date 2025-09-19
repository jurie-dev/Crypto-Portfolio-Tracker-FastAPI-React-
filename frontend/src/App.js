import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Portfolio from "./components/Portfolio";
import AddMoney from "./components/AddMoney";
import Trade from "./components/Trade";

function App() {
  const token = localStorage.getItem("token");

  return (
    <Router>
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <Routes>
          <Route path="/login" element={!token ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!token ? <Register /> : <Navigate to="/dashboard" />} />
          <Route
            path="/dashboard"
            element={
              token ? (
                <div className="max-w-3xl w-full p-6 bg-white shadow rounded-xl space-y-6">
                  <h1 className="text-2xl font-bold text-center">Crypto Portfolio Tracker</h1>
                  <AddMoney />
                  <Trade />
                  <Portfolio />
                  <button
                    onClick={() => {
                      localStorage.removeItem("token");
                      window.location.href = "/login";
                    }}
                    className="mt-4 w-full bg-red-500 text-white py-2 rounded-lg"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <Navigate to="/login" />
              )
            }
          />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
