'use client'

import { useEffect, useState } from 'react'
import { vizApi } from '@/lib/api'
import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowRight,
  Bell,
  Bot,
  BrainCircuit,
  Building2,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  CircleDollarSign,
  Clock3,
  Database,
  Download,
  Globe2,
  GraduationCap,
  HandCoins,
  HeartPulse,
  Home,
  Info,
  Landmark,
  LayoutDashboard,
  Lightbulb,
  LineChart,
  Map,
  Menu,
  Network,
  PackageOpen,
  PanelLeftClose,
  Search,
  Settings2,
  ShieldCheck,
  ShoppingCart,
  Sparkles,
  Target,
  Users,
  X,
  Zap,
} from 'lucide-react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart as RechartsLineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const logo = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/ChatGPT%20Image%20Aug%208%2C%202026%2C%2012_10_21%20AM-25y7spyU8PJWD9FH90HZXV9NaFsXvl.png'

const navItems = [
  ['Overview', LayoutDashboard], ['AI Student Digital Twin', Bot], ['Intervention Simulator', CircleDollarSign], ['AI Policy Simulator', Landmark], ['Risk Explanation', Info], ['Future School Simulator', Building2], ['Resource Allocation', HandCoins], ['Intervention Marketplace', ShoppingCart], ['Student Journey Timeline', Clock3], ['AI Fairness Auditor', ShieldCheck], ['Heatmap', Map], ['AI Root Cause Graph', Network], ['Multi-Agent Council', BrainCircuit], ['Early Warning Horizon', Target], ['Opportunity Detector', Lightbulb], ['App Quality Guardian', HeartPulse],
] as const

const fallbackTrendData = [
  { month: 'Jan', low: 58, medium: 34, high: 14, critical: 3 }, { month: 'Feb', low: 64, medium: 31, high: 16, critical: 3 }, { month: 'Mar', low: 56, medium: 34, high: 13, critical: 3 }, { month: 'Apr', low: 59, medium: 32, high: 12, critical: 3 }, { month: 'May', low: 61, medium: 30, high: 11, critical: 3 }, { month: 'Jun', low: 65, medium: 32, high: 9, critical: 3 }, { month: 'Jul', low: 60, medium: 30, high: 12, critical: 3 }, { month: 'Aug', low: 61, medium: 31, high: 12, critical: 3 }, { month: 'Sep', low: 60, medium: 31, high: 13, critical: 3 }, { month: 'Oct', low: 64, medium: 29, high: 11, critical: 3 }, { month: 'Nov', low: 60, medium: 29, high: 12, critical: 3 }, { month: 'Dec', low: 54, medium: 30, high: 12, critical: 3 },
]
const fallbackFactors = [['Low Attendance', 42, 'var(--risk-critical)'], ['Low Test Scores', 37, 'var(--risk-blue)'], ['Low Household Income', 31, 'var(--risk-teal)'], ['Large Distance to School', 22, 'var(--risk-purple)'], ['No Internet Access', 19, 'var(--risk-pink)']] as const
const factorColors = ['var(--risk-critical)', 'var(--risk-blue)', 'var(--risk-teal)', 'var(--risk-purple)', 'var(--risk-pink)']
const spark = [2, 4, 3, 6, 4, 7, 5, 8, 6, 9, 7, 10]

function MiniSpark({ color }: { color: string }) {
  return <ResponsiveContainer width="100%" height="100%"><AreaChart data={spark.map((value, index) => ({ index, value }))}><Area type="monotone" dataKey="value" stroke={color} fill={color} fillOpacity={0.04} strokeWidth={1.5} dot={false} /></AreaChart></ResponsiveContainer>
}

function MetricCard({ icon: Icon, label, value, note, color, tone }: { icon: typeof Users; label: string; value: string; note: string; color: string; tone: string }) {
  return <section className="metric-card"><div className="metric-top"><div className="metric-icon" style={{ color, background: `color-mix(in srgb, ${color} 12%, white)` }}><Icon size={22} /></div><div><p className="metric-label">{label}</p><p className="metric-value">{value}</p><p className="metric-note" style={{ color: tone }}>{note}</p></div></div><div className="spark"><MiniSpark color={color} /></div></section>
}

function Card({ title, children, className = '', action }: { title: React.ReactNode; children: React.ReactNode; className?: string; action?: React.ReactNode }) {
  return <section className={`panel ${className}`}><div className="panel-heading"><h2>{title}</h2>{action}</div>{children}</section>
}

function RiskDistribution({ summary }: { summary?: any }) {
  const total = summary?.total_students ?? 200000
  const risk = summary?.risk ?? {}
  const data = [
    { name: 'Low Risk', key: 'Low', value: risk.Low?.percent ?? 49.4, count: risk.Low?.count ?? 98732, color: 'var(--risk-low)' },
    { name: 'Medium Risk', key: 'Medium', value: risk.Medium?.percent ?? 31.2, count: risk.Medium?.count ?? 62415, color: 'var(--risk-medium)' },
    { name: 'High Risk', key: 'High', value: risk.High?.percent ?? 14.2, count: risk.High?.count ?? 28457, color: 'var(--risk-high)' },
    { name: 'Critical Risk', key: 'Critical', value: risk.Critical?.percent ?? 5.2, count: risk.Critical?.count ?? 10396, color: 'var(--risk-critical)' },
  ]
  return <div className="distribution"><div className="donut-wrap"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={data} dataKey="value" innerRadius="58%" outerRadius="82%" paddingAngle={1} stroke="white" strokeWidth={2}>{data.map((entry) => <Cell key={entry.name} fill={entry.color} />)}</Pie></PieChart></ResponsiveContainer><div className="donut-label"><strong>{Number(total).toLocaleString()}</strong><span>Students</span></div></div><div className="legend-list">{data.map((item) => <div className="legend-item" key={item.name}><i style={{ background: item.color }} /><span>{item.name}<b>{Number(item.count).toLocaleString()}</b><small>({item.value}%)</small></span></div>)}</div></div>
}

function TrendChart({ data }: { data?: any[] }) {
  const chartData = data?.length ? data.map((item) => ({ ...item, month: String(item.month).slice(5) })) : fallbackTrendData
  return <div className="trend-chart"><ResponsiveContainer width="100%" height="100%"><RechartsLineChart data={chartData} margin={{ left: -24, right: 4, top: 6, bottom: 0 }}><CartesianGrid vertical={false} stroke="var(--border)" /><XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: 'var(--muted-foreground)', fontSize: 10 }} /><YAxis tickLine={false} axisLine={false} tick={{ fill: 'var(--muted-foreground)', fontSize: 10 }} domain={[0, 100]} /><Tooltip /><Line dataKey="low" stroke="var(--risk-low)" strokeWidth={2} dot={{ r: 2 }} /><Line dataKey="medium" stroke="var(--risk-medium)" strokeWidth={2} dot={{ r: 2 }} /><Line dataKey="high" stroke="var(--risk-high)" strokeWidth={2} dot={{ r: 2 }} /><Line dataKey="critical" stroke="var(--risk-critical)" strokeWidth={2} dot={{ r: 2 }} /></RechartsLineChart></ResponsiveContainer><div className="chart-legend"><span className="low">● Low Risk</span><span className="medium">● Medium Risk</span><span className="high">● High Risk</span><span className="critical">● Critical Risk</span></div></div>
}

export default function Page() {
  const [active, setActive] = useState('Overview')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [toast, setToast] = useState('')
  const [overview, setOverview] = useState<any>(null)
  const [factorData, setFactorData] = useState<any[]>([])
  const [apiConnected, setApiConnected] = useState(false)
  const notify = (message: string) => { setToast(message); window.setTimeout(() => setToast(''), 2200) }

  useEffect(() => {
    Promise.all([vizApi.overview(), vizApi.factors()])
      .then(([overviewResponse, factorResponse]) => {
        setOverview(overviewResponse)
        setFactorData(factorResponse?.factors ?? [])
        setApiConnected(Boolean(overviewResponse?.model_status?.loaded))
      })
      .catch(() => setApiConnected(false))
  }, [])

  const summary = overview?.summary
  const risk = summary?.risk ?? {}
  const totalStudents = summary?.total_students ?? 200000
  const displayFactors = factorData.length
    ? factorData.slice(0, 5).map((item, index) => [String(item.feature).replaceAll('_', ' '), Number(item.percent), factorColors[index % factorColors.length]] as const)
    : fallbackFactors
  return <main className="dashboard-shell">
    <aside className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
      <div className="brand"><a href="/" aria-label="VIZHIPPAAN dashboard home"><img src={logo} alt="VIZHIPPAAN Child Education Risk Intelligence Platform" /></a><button className="icon-button sidebar-toggle" onClick={() => setSidebarOpen(false)} aria-label="Collapse navigation"><PanelLeftClose size={17} /></button></div>
      <nav aria-label="Primary navigation">{navItems.map(([label, Icon]) => <button key={label} className={`nav-item ${active === label ? 'active' : ''}`} onClick={() => { setActive(label); notify(`${label} selected`) }}><Icon size={17} /><span>{label}</span></button>)}</nav>
      <div className="admin-card"><div className="admin-avatar"><Users size={20} /></div><div><strong>Admin User</strong><span>District Admin</span></div><ChevronDown size={15} /></div>
    </aside>
    <div className="main-area">
      <header className="topbar"><div className="welcome"><button className="mobile-menu icon-button" onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Toggle navigation"><Menu size={20} /></button><div><h1>Welcome back, Admin! <span>👋</span></h1><p>Empowering every child to stay, learn and thrive.</p></div></div><div className="top-actions"><button className="select-button">Academic Year<strong>2025 - 2026</strong><ChevronDown size={15} /></button><button className="select-button">District<strong>All Districts</strong><ChevronDown size={15} /></button><button className="notification icon-button" onClick={() => notify('You have 3 new alerts')} aria-label="Notifications"><Bell size={20} /><b>3</b></button><button className="export-button" onClick={() => notify('Report export started')}><Download size={16} /> Export Report</button></div></header>
      <div className="content">
        <div className="metric-grid"><MetricCard icon={Users} label="Total Students" value={Number(totalStudents).toLocaleString()} note={apiConnected ? "Live dataset" : "Backend fallback"} color="var(--risk-purple)" tone="var(--success)" /><MetricCard icon={ShieldCheck} label="Low Risk" value={Number(risk.Low?.count ?? 98732).toLocaleString()} note={`${risk.Low?.percent ?? 49.4}% of students`} color="var(--risk-low)" tone="var(--muted-foreground)" /><MetricCard icon={AlertTriangle} label="Medium Risk" value={Number(risk.Medium?.count ?? 62415).toLocaleString()} note={`${risk.Medium?.percent ?? 31.2}% of students`} color="var(--risk-medium)" tone="var(--muted-foreground)" /><MetricCard icon={AlertTriangle} label="High Risk" value={Number(risk.High?.count ?? 28457).toLocaleString()} note={`${risk.High?.percent ?? 14.2}% of students`} color="var(--risk-high)" tone="var(--muted-foreground)" /><MetricCard icon={AlertTriangle} label="Critical Risk" value={Number(risk.Critical?.count ?? 10396).toLocaleString()} note={`${risk.Critical?.percent ?? 5.2}% of students`} color="var(--risk-critical)" tone="var(--muted-foreground)" /></div>
        <div className="grid-row row-one"><Card title="Risk Distribution" className="distribution-card"><RiskDistribution summary={summary} /></Card><Card title="Risk Trend Over Time" className="trend-card"><TrendChart data={overview?.risk_trend} /></Card><Card title="Top Risk Factors (Overall)" className="factors-card"><div className="factor-list">{displayFactors.map(([name, value, color]) => <div className="factor-row" key={name}><span>{name}</span><div className="factor-bar"><i style={{ width: `${value}%`, background: color }} /></div><b>{value}%</b></div>)}</div><button className="outline-button" onClick={() => notify('Showing all risk factors')}>View All Factors <ArrowRight size={15} /></button></Card></div>
        <div className="grid-row row-two"><Card title="District Risk Heatmap" className="heatmap-card"><div className="map-placeholder"><div className="map-grid" /><div className="map-shape"><span /><span /><span /><span /><span /><span /><span /><span /><span /></div><div className="map-controls"><button onClick={() => notify('Map zoomed in')}>+</button><button onClick={() => notify('Map zoomed out')}>−</button><button onClick={() => notify('Map reset')}>⌗</button></div><div className="map-key"><strong>Risk Level</strong><span><i className="low-dot" /> Low</span><span><i className="medium-dot" /> Medium</span><span><i className="high-dot" /> High</span><span><i className="critical-dot" /> Critical</span></div></div><button className="outline-button map-button" onClick={() => notify('Opening full district map')}>View Full Map</button></Card><Card title={< >Intervention Impact <em>(Simulator Preview)</em></>} className="intervention-card"><div className="intervention-list">{[['Scholarship Program', '18.6%'], ['Counselling Support', '14.2%'], ['Attendance Support', '12.7%'], ['Free Meal Program', '9.8%'], ['Remedial Classes', '8.1%']].map(([name, value], i) => <div key={name}><span><i className={`impact-icon i-${i}`} />{name}</span><b>↓ {value}</b></div>)}</div><button className="primary-button" onClick={() => notify('Simulator ready')}>Run Simulator</button></Card><Card title="Alerts & Early Warnings" className="alerts-card" action={<button className="text-button" onClick={() => notify('Showing all alerts')}>View All</button>}><div className="alerts-list">{[['1,250 students moved to High Risk', 'in the last 7 days', 'alert-red', AlertTriangle], ['342 students at risk of dropout', 'within next 30 days', 'alert-orange', AlertTriangle], ['5 schools require immediate attention', 'High risk concentration detected', 'alert-yellow', Zap], ['Data quality issues detected', '3 datasets need review', 'alert-blue', Database]].map(([a, b, tone, Icon]) => <button key={a as string} className={`alert ${tone}`} onClick={() => notify(a as string)}><Icon size={17} /><span><strong>{a}</strong><small>{b}</small></span><ChevronRight size={16} /></button>)}</div></Card></div>
        <div className="grid-row row-three"><Card title="Opportunity Detector" className="utility-card opportunity"><div className="opportunity-body"><div className="progress-ring"><svg viewBox="0 0 42 42"><circle cx="21" cy="21" r="15.9" /><circle className="progress" cx="21" cy="21" r="15.9" /></svg><strong>72%</strong><span>High Potential</span></div><p><b>14,856 students</b> can significantly improve with right support</p></div><button className="outline-button" onClick={() => notify('Showing opportunities')}>View Opportunities</button></Card><Card title="AI Fairness Auditor" className="utility-card"><div className="audit-stat"><span>Gender Parity Difference</span><b>2.6% <em>(Good)</em></b><CheckCircle2 size={20} /></div><div className="audit-stat bottom"><span>Groups Monitored</span><b><Users size={16} /> 6</b></div><button className="outline-button" onClick={() => notify('Opening fairness report')}>View Report</button></Card><Card title={< >Resource Allocation <em>(AI Optimizer)</em></>} className="utility-card resource"><p className="small-heading">Optimal Allocation Suggestion</p><div className="resource-grid">{[['Scholarships', '2,450', GraduationCap], ['Counsellors', '120', Users], ['Devices', '1,820', PackageOpen], ['Meals', '5,600', HandCoins]].map(([name, value, Icon]) => <div key={name as string}><Icon size={17} /><span>{name}</span><b>{value}</b></div>)}</div><button className="outline-button" onClick={() => notify('Opening allocation plan')}>View Allocation Plan</button></Card><Card title="System Health" className="utility-card health"><div className="health-list">{[['Model Status', overview?.model_status?.loaded ? 'Healthy' : 'Offline', CheckCircle2], ['API Status', apiConnected ? 'Healthy' : 'Offline', CheckCircle2], ['Data Pipeline', summary ? 'Healthy' : 'Offline', Database], ['Last Updated', apiConnected ? 'Live' : 'Waiting', Clock3]].map(([name, value, Icon]) => <div key={name as string}><span><Icon size={15} /> {name}</span><b className={value === 'Healthy' ? 'healthy' : ''}>{value}</b></div>)}</div><button className="outline-button" onClick={() => notify('Opening system dashboard')}>System Dashboard</button></Card></div>
      </div>
      <footer><span><span className="heart">♥</span> Every child has potential. VIZHIPPAAN ensures no child is left behind.</span><span>VIZHIPPAAN © 2025 <i /> AI for Social Good</span></footer>
    </div>
    {toast && <div className="toast"><CheckCircle2 size={16} /> {toast}</div>}
  </main>
}
