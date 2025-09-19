import React, { useState } from "react";
import API from "../api/api";

function Trade() {
  const [symbol, setSymbol] = useState("");
  const [quantity, setQuantity] = useState("");

  const buy = async () => {
    try {
      await API.post("/buy", { symbol, quantity: parseFloat(quantity) });
      alert("Bought asset!");
    } catch {
      alert("Error buying!");
    }
  };

  const sell = async () => {
    try {
      await API.post("/sell", { symbol, quantity: parseFloat(quantity) });
      alert("Sold asset!");
    } catch {
      alert("Error selling!");
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">Trade</h3>
      <div className="flex space-x-2 mb-2">
        <input
          placeholder="Symbol (e.g. BTC)"
          className="flex-1 p-2 border rounded-lg"
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        />
        <input
          type="number"
          placeholder="Quantity"
          className="flex-1 p-2 border rounded-lg"
          onChange={(e) => setQuantity(e.target.value)}
        />
      </div>
      <div className="flex space-x-2">
        <button
          onClick={buy}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
        >
          Buy
        </button>
        <button
          onClick={sell}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
        >
          Sell
        </button>
      </div>
    </div>
  );
}

export default Trade;
