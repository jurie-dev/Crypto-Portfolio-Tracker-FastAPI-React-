import React, { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await API.post("/register", { username, password });
      alert("User registered successfully!");
      navigate("/login");
    } catch (err) {
      alert("Registration failed!");
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-8 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
      <form onSubmit={handleRegister} className="space-y-4">
        <input
          className="w-full p-2 border rounded-lg"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="w-full p-2 border rounded-lg"
          placeholder="Password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600">
          Register
        </button>
      </form>
      <p className="mt-4 text-center text-sm">
        Already have an account?{" "}
        <span
          className="text-blue-500 cursor-pointer"
          onClick={() => navigate("/login")}
        >
          Login
        </span>
      </p>
    </div>
  );
}

export default Register;
