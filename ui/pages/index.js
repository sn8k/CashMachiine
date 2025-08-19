/** Home page v0.2.0 (2025-08-19) */
import Link from 'next/link';

export default function Home() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">CashMachiine UI</h1>
      <ul className="list-disc ml-5">
        <li><Link href="/goals">Create Goal</Link></li>
        <li><Link href="/daily-actions">Daily Actions</Link></li>
      </ul>
    </div>
  );
}
