/** Goal creation page v0.2.0 (2025-08-19) */
import { useState } from 'react';

export default function Goals() {
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');

  const submitGoal = async (e) => {
    e.preventDefault();
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/goals`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    });
    setMessage(res.ok ? 'Goal created!' : 'Error creating goal');
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Create Goal</h1>
      <form onSubmit={submitGoal} className="space-y-4">
        <input
          className="border p-2 w-full"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Goal name"
        />
        <button className="bg-blue-500 text-white px-4 py-2" type="submit">Create</button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
}
