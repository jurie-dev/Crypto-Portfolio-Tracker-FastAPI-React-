import React, { useState } from "react";
import API from "../api/api";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const res = await API.post("/token", formData);
      localStorage.setItem("token", res.data.access_token);

      // Force redirect so dashboard reloads with token
      window.location.href = "/dashboard";
    } catch (err) {
      alert("Login failed!");
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-8 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
      <form onSubmit={handleLogin} className="space-y-4">
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
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
        >
          Login
        </button>
      </form>
      <p className="mt-4 text-center text-sm">
        Don’t have an account?{" "}
        <span
          className="text-blue-500 cursor-pointer"
          onClick={() => (window.location.href = "/register")}
        >
          Register
        </span>
      </p>
    </div>
  );
}

export default Login;
