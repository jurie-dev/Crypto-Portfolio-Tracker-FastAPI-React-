import React, { useEffect, useState } from "react";
import API from "../api/api";

function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);

// In Portfolio.js
const fetchPortfolio = async () => {
  try {
    const res = await API.get("/portfolio");
    setPortfolio(res.data);
  } catch (err) {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    } else {
      alert("Error fetching portfolio!");
    }
  }
};


  useEffect(() => {
    fetchPortfolio();
  }, []);

  return (
    <div className="p-4 border rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">My Portfolio</h2>
      {portfolio ? (
        <div>
          <p>Total Value: ${portfolio.total_value.toFixed(2)}</p>
          <p>Available Money: ${portfolio.available_money.toFixed(2)}</p>
          <h3 className="mt-4 font-semibold">Assets</h3>
          <ul className="list-disc list-inside">
            {portfolio.assets.map((asset, idx) => (
              <li key={idx}>
                {asset.symbol} | Qty: {asset.quantity} | Value: $
                {asset.total_value.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No portfolio yet.</p>
      )}
    </div>
  );
}

export default Portfolio;
