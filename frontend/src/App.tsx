import { useEffect, useMemo, useState } from "react";
import { NavLink, Route, Routes } from "react-router";
import { api, Dashboard, EntitySummary, SystemSummary } from "./api";

const navigation = [
  ["Overview", "/"], ["Proposals", "/proposals"], ["Specifications", "/specifications"],
  ["Tasks", "/tasks"], ["Runs", "/runs"], ["Reviews", "/reviews"],
  ["Approvals", "/approvals"], ["System", "/system"],
] as const;

function EntityTable({ title, rows }: { title: string; rows: EntitySummary[] }) {
  return <section className="panel">
    <div className="panelHeader"><div><span className="eyebrow">Control plane</span><h2>{title}</h2></div><span className="count">{rows.length}</span></div>
    {rows.length === 0 ? <div className="empty"><strong>No {title.toLowerCase()} yet</strong><span>This surface is connected to the canonical runtime API.</span></div> :
      <div>{rows.map((row) => <div className="tableRow" key={row.id}><div><strong>{row.title}</strong><span>{row.id}</span></div><span className="status">{row.status}</span></div>)}</div>}
  </section>;
}

function Overview({ dashboard }: { dashboard: Dashboard }) {
  const cards = [["Proposals", dashboard.proposals.length], ["Specifications", dashboard.specifications.length], ["Tasks", dashboard.tasks.length], ["Runs", dashboard.runs.length], ["Reviews", dashboard.reviews.length], ["Approvals", dashboard.approvals.length]];
  return <>
    <section className="hero"><div><span className="eyebrow">Human Control Plane</span><h1>Develop Control</h1><p>One operational view over specifications, work, evidence, review and human gates.</p></div><div className="revision"><span>State revision</span><strong>{dashboard.state_revision}</strong></div></section>
    <section className="metricGrid">{cards.map(([label, value]) => <article className="metric" key={label}><span>{label}</span><strong>{value}</strong></article>)}</section>
    <section className="panel"><span className="eyebrow">Operating model</span><h2>End-state surfaces from day one</h2><div className="flow"><span>Proposal</span><b>→</b><span>Specification</span><b>→</b><span>Task</span><b>→</b><span>Run</span><b>→</b><span>Tests</span><b>→</b><span>Review</span><b>→</b><span>Approval</span></div></section>
  </>;
}

function SystemPage({ system }: { system: SystemSummary | null }) {
  if (!system) return <section className="panel">Loading system view…</section>;
  return <section className="panel"><div className="panelHeader"><div><span className="eyebrow">Read-mostly</span><h2>System</h2></div><span className="status">{system.status}</span></div><div className="systemGrid"><div><span>Environment</span><strong>{system.environment}</strong></div><div><span>State backend</span><strong>{system.state_backend}</strong></div></div><h3>Capabilities</h3><div className="capabilities">{Object.entries(system.capabilities).map(([name,status]) => <div key={name}><span>{name.replaceAll("_", " ")}</span><strong>{status}</strong></div>)}</div></section>;
}

export function App() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [system, setSystem] = useState<SystemSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { Promise.all([api.dashboard(), api.system()]).then(([d,s]) => { setDashboard(d); setSystem(s); }).catch((err: Error) => setError(err.message)); }, []);
  const state = useMemo(() => dashboard ?? { schema_version: 1, state_revision: 0, last_event_sequence: 0, proposals: [], specifications: [], tasks: [], runs: [], reviews: [], approvals: [] }, [dashboard]);
  return <div className="shell"><aside className="sidebar"><div className="brand"><span className="brandMark">S</span><div><strong>ScoreSymphony</strong><span>Agent Platform</span></div></div><nav>{navigation.map(([label,path]) => <NavLink key={path} to={path} end={path === "/"}>{label}</NavLink>)}</nav><div className="sidebarFooter"><span>Runtime API</span><strong className={error ? "offline" : "online"}>{error ? "Unavailable" : "Connected"}</strong></div></aside><main>{error && <div className="errorBanner">API error: {error}</div>}<Routes><Route path="/" element={<Overview dashboard={state} />} /><Route path="/proposals" element={<EntityTable title="Proposals" rows={state.proposals} />} /><Route path="/specifications" element={<EntityTable title="Specifications" rows={state.specifications} />} /><Route path="/tasks" element={<EntityTable title="Tasks" rows={state.tasks} />} /><Route path="/runs" element={<EntityTable title="Runs" rows={state.runs} />} /><Route path="/reviews" element={<EntityTable title="Reviews" rows={state.reviews} />} /><Route path="/approvals" element={<EntityTable title="Approvals" rows={state.approvals} />} /><Route path="/system" element={<SystemPage system={system} />} /></Routes></main></div>;
}
