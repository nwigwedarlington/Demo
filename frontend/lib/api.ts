export type Job = {
  id: string;
  url: string;
  source_type: string;
  status: string;
  attempts: number;
  last_error?: string | null;
  created_at: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function getJobs(): Promise<Job[]> {
  const response = await fetch(`${API_BASE_URL}/jobs`, { cache: "no-store" });
  if (!response.ok) return [];
  return response.json();
}
