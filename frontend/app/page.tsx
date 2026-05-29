import { Activity, AlertTriangle, Bot, RefreshCw, Server, ShieldCheck } from "lucide-react";

import { getJobs } from "../lib/api";

const statusTone: Record<string, string> = {
  queued: "bg-zinc-200 text-zinc-800",
  processing: "bg-blue-100 text-blue-900",
  completed: "bg-emerald-100 text-emerald-900",
  failed: "bg-red-100 text-red-900"
};

export default async function Dashboard() {
  const jobs = await getJobs();
  const failed = jobs.filter((job) => job.status === "failed").length;
  const completed = jobs.filter((job) => job.status === "completed").length;
  const processing = jobs.filter((job) => job.status === "processing").length;

  return (
    <main className="min-h-screen">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal">Fact-Check Ops</h1>
            <p className="mt-1 text-sm text-zinc-600">Facebook monitoring, AI verification, alerts, and publishing.</p>
          </div>
          <div className="flex gap-2">
            <button className="grid h-10 w-10 place-items-center rounded border border-zinc-300 bg-white" title="Refresh">
              <RefreshCw size={18} />
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-6 py-6 md:grid-cols-4">
        <Metric icon={<Activity size={18} />} label="Queue" value={jobs.length} />
        <Metric icon={<ShieldCheck size={18} />} label="Completed" value={completed} />
        <Metric icon={<Bot size={18} />} label="Processing" value={processing} />
        <Metric icon={<AlertTriangle size={18} />} label="Failures" value={failed} />
      </section>

      <section className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-6 pb-8 lg:grid-cols-[1fr_340px]">
        <div className="overflow-hidden rounded-lg border border-zinc-200 bg-white">
          <div className="border-b border-zinc-200 px-4 py-3">
            <h2 className="text-base font-semibold">Jobs</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-zinc-50 text-zinc-600">
                <tr>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Source</th>
                  <th className="px-4 py-3 font-medium">Attempts</th>
                  <th className="px-4 py-3 font-medium">Created</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((job) => (
                  <tr key={job.id} className="border-t border-zinc-100">
                    <td className="px-4 py-3">
                      <span className={`rounded px-2 py-1 text-xs ${statusTone[job.status] || "bg-zinc-100"}`}>
                        {job.status}
                      </span>
                    </td>
                    <td className="max-w-[560px] truncate px-4 py-3 text-zinc-700">{job.url}</td>
                    <td className="px-4 py-3">{job.attempts}</td>
                    <td className="px-4 py-3 text-zinc-600">{new Date(job.created_at).toLocaleString()}</td>
                  </tr>
                ))}
                {!jobs.length && (
                  <tr>
                    <td className="px-4 py-10 text-center text-zinc-500" colSpan={4}>
                      No jobs yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <aside className="rounded-lg border border-zinc-200 bg-white p-4">
          <div className="mb-4 flex items-center gap-2">
            <Server size={18} />
            <h2 className="text-base font-semibold">Provider Health</h2>
          </div>
          <HealthRow label="API Gateway" value="online" />
          <HealthRow label="Queue Worker" value="redis-backed" />
          <HealthRow label="AI Provider" value="failover ready" />
          <HealthRow label="Telegram Alerts" value="env-configured" />
        </aside>
      </section>
    </main>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-4">
      <div className="flex items-center justify-between text-zinc-600">
        {icon}
        <span className="text-xs uppercase">{label}</span>
      </div>
      <div className="mt-4 text-3xl font-semibold">{value}</div>
    </div>
  );
}

function HealthRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-t border-zinc-100 py-3 text-sm first:border-t-0">
      <span className="text-zinc-600">{label}</span>
      <span className="rounded bg-emerald-100 px-2 py-1 text-xs text-emerald-900">{value}</span>
    </div>
  );
}
