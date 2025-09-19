import React, { useState } from "react";
import API from "../api/api";

function AddMoney() {
  const [amount, setAmount] = useState("");

  const handleAdd = async () => {
    try {
      const res = await API.post("/add-money", { amount: parseFloat(amount) });
      alert("Added money! Available: " + res.data.available_money);
    } catch (err) {
      alert("Error adding money!");
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-2">Add Money</h3>
      <div className="flex space-x-2">
        <input
          type="number"
          placeholder="Amount"
          className="flex-1 p-2 border rounded-lg"
          onChange={(e) => setAmount(e.target.value)}
        />
        <button
          onClick={handleAdd}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Add
        </button>
      </div>
    </div>
  );
}

export default AddMoney;
