export type EntitySummary = { id: string; title: string; status: string; updated_at: string; meta: Record<string, unknown> };
export type Dashboard = {
  schema_version: number; state_revision: number; last_event_sequence: number;
  proposals: EntitySummary[]; specifications: EntitySummary[]; tasks: EntitySummary[];
  runs: EntitySummary[]; reviews: EntitySummary[]; approvals: EntitySummary[];
};
export type SystemSummary = {
  environment: string; state_backend: string; status: "healthy" | "degraded" | "blocked";
  workers: Array<Record<string, unknown>>; capabilities: Record<string, string>;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json() as Promise<T>;
}

export const api = {
  dashboard: () => getJson<Dashboard>("/api/v1/dashboard"),
  system: () => getJson<SystemSummary>("/api/v1/system"),
};
