'use client'

import {
  useEffect,
  useState,
  type ElementType,
  type ReactNode,
} from 'react'

import { vizApi } from '@/lib/api'

import {
  AlertTriangle,
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
  GraduationCap,
  HandCoins,
  HeartPulse,
  Info,
  Landmark,
  LayoutDashboard,
  Lightbulb,
  Map,
  Menu,
  Network,
  PackageOpen,
  PanelLeftClose,
  ShieldCheck,
  ShoppingCart,
  Target,
  Users,
  Zap,
} from 'lucide-react'

import {
  Area,
  AreaChart,
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

/* ============================================================
   LOGO
============================================================ */

const logo =
  'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/ChatGPT%20Image%20Aug%208%2C%202026%2C%2012_10_21%20AM-25y7spyU8PJWD9FH90HZXV9NaFsXvl.png'

/* ============================================================
   SIDEBAR MODULE CONFIGURATION
============================================================ */

type NavigationItem = {
  label: string
  icon: ElementType
}

type NavigationModule = {
  label: string
  icon: ElementType
  items: NavigationItem[]
}

const navigationModules: NavigationModule[] = [
  {
    label: 'Student Intelligence',
    icon: Users,
    items: [
      {
        label: 'AI Student Digital Twin',
        icon: Bot,
      },
      {
        label: 'Student Journey Timeline',
        icon: Clock3,
      },
      {
        label: 'Risk Explanation',
        icon: Info,
      },
      {
        label: 'Early Warning Horizon',
        icon: Target,
      },
    ],
  },

  {
    label: 'Predictive Intelligence',
    icon: BrainCircuit,
    items: [
      {
        label: 'AI Root Cause Graph',
        icon: Network,
      },
      {
        label: 'Future School Simulator',
        icon: Building2,
      },
      {
        label: 'Opportunity Detector',
        icon: Lightbulb,
      },
    ],
  },

  {
    label: 'Intervention Intelligence',
    icon: Target,
    items: [
      {
        label: 'Intervention Simulator',
        icon: CircleDollarSign,
      },
      {
        label: 'Resource Allocation',
        icon: HandCoins,
      },
      {
        label: 'Intervention Marketplace',
        icon: ShoppingCart,
      },
    ],
  },

  {
    label: 'Policy & Decision Intelligence',
    icon: Landmark,
    items: [
      {
        label: 'AI Policy Simulator',
        icon: Landmark,
      },
      {
        label: 'Heatmap',
        icon: Map,
      },
    ],
  },

  {
    label: 'Responsible AI',
    icon: ShieldCheck,
    items: [
      {
        label: 'AI Fairness Auditor',
        icon: ShieldCheck,
      },
      {
        label: 'Multi-Agent Council',
        icon: BrainCircuit,
      },
      {
        label: 'App Quality Guardian',
        icon: HeartPulse,
      },
    ],
  },
]

/* ============================================================
   FALLBACK DATA
============================================================ */

const fallbackTrendData = [
  {
    month: 'Jan',
    low: 58,
    medium: 34,
    high: 14,
    critical: 3,
  },
  {
    month: 'Feb',
    low: 64,
    medium: 31,
    high: 16,
    critical: 3,
  },
  {
    month: 'Mar',
    low: 56,
    medium: 34,
    high: 13,
    critical: 3,
  },
  {
    month: 'Apr',
    low: 59,
    medium: 32,
    high: 12,
    critical: 3,
  },
  {
    month: 'May',
    low: 61,
    medium: 30,
    high: 11,
    critical: 3,
  },
  {
    month: 'Jun',
    low: 65,
    medium: 32,
    high: 9,
    critical: 3,
  },
  {
    month: 'Jul',
    low: 60,
    medium: 30,
    high: 12,
    critical: 3,
  },
  {
    month: 'Aug',
    low: 61,
    medium: 31,
    high: 12,
    critical: 3,
  },
  {
    month: 'Sep',
    low: 60,
    medium: 31,
    high: 13,
    critical: 3,
  },
  {
    month: 'Oct',
    low: 64,
    medium: 29,
    high: 11,
    critical: 3,
  },
  {
    month: 'Nov',
    low: 60,
    medium: 29,
    high: 12,
    critical: 3,
  },
  {
    month: 'Dec',
    low: 54,
    medium: 30,
    high: 12,
    critical: 3,
  },
]

const fallbackFactors = [
  [
    'Low Attendance',
    42,
    'var(--risk-critical)',
  ],
  [
    'Low Test Scores',
    37,
    'var(--risk-blue)',
  ],
  [
    'Low Household Income',
    31,
    'var(--risk-teal)',
  ],
  [
    'Large Distance to School',
    22,
    'var(--risk-purple)',
  ],
  [
    'No Internet Access',
    19,
    'var(--risk-pink)',
  ],
] as const

const factorColors = [
  'var(--risk-critical)',
  'var(--risk-blue)',
  'var(--risk-teal)',
  'var(--risk-purple)',
  'var(--risk-pink)',
]

const spark = [
  2,
  4,
  3,
  6,
  4,
  7,
  5,
  8,
  6,
  9,
  7,
  10,
]

/* ============================================================
   MINI SPARKLINE
============================================================ */

function MiniSpark({
  color,
}: {
  color: string
}) {
  const data = spark.map(
    (value, index) => ({
      index,
      value,
    })
  )

  return (
    <ResponsiveContainer
      width="100%"
      height="100%"
    >
      <AreaChart data={data}>
        <Area
          type="monotone"
          dataKey="value"
          stroke={color}
          fill={color}
          fillOpacity={0.04}
          strokeWidth={1.5}
          dot={false}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

/* ============================================================
   METRIC CARD
============================================================ */

function MetricCard({
  icon: Icon,
  label,
  value,
  note,
  color,
  tone,
}: {
  icon: ElementType
  label: string
  value: string
  note: string
  color: string
  tone: string
}) {
  return (
    <section className="metric-card">
      <div className="metric-top">
        <div
          className="metric-icon"
          style={{
            color,
            background: `color-mix(in srgb, ${color} 12%, white)`,
          }}
        >
          <Icon size={22} />
        </div>

        <div>
          <p className="metric-label">
            {label}
          </p>

          <p className="metric-value">
            {value}
          </p>

          <p
            className="metric-note"
            style={{
              color: tone,
            }}
          >
            {note}
          </p>
        </div>
      </div>

      <div className="spark">
        <MiniSpark color={color} />
      </div>
    </section>
  )
}

/* ============================================================
   GENERIC DASHBOARD CARD
============================================================ */

function Card({
  title,
  children,
  className = '',
  action,
}: {
  title: ReactNode
  children: ReactNode
  className?: string
  action?: ReactNode
}) {
  return (
    <section
      className={`panel ${className}`}
    >
      <div className="panel-heading">
        <h2>{title}</h2>

        {action}
      </div>

      {children}
    </section>
  )
}

/* ============================================================
   RISK DISTRIBUTION
============================================================ */

function RiskDistribution({
  summary,
}: {
  summary?: any
}) {
  const total =
    summary?.total_students ?? 200000

  const risk =
    summary?.risk ?? {}

  const data = [
    {
      name: 'Low Risk',
      value:
        risk.Low?.percent ?? 49.4,
      count:
        risk.Low?.count ?? 98732,
      color: 'var(--risk-low)',
    },
    {
      name: 'Medium Risk',
      value:
        risk.Medium?.percent ?? 31.2,
      count:
        risk.Medium?.count ?? 62415,
      color: 'var(--risk-medium)',
    },
    {
      name: 'High Risk',
      value:
        risk.High?.percent ?? 14.2,
      count:
        risk.High?.count ?? 28457,
      color: 'var(--risk-high)',
    },
    {
      name: 'Critical Risk',
      value:
        risk.Critical?.percent ?? 5.2,
      count:
        risk.Critical?.count ?? 10396,
      color:
        'var(--risk-critical)',
    },
  ]

  return (
    <div className="distribution">
      <div className="donut-wrap">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              innerRadius="58%"
              outerRadius="82%"
              paddingAngle={1}
              stroke="white"
              strokeWidth={2}
            >
              {data.map((entry) => (
                <Cell
                  key={entry.name}
                  fill={entry.color}
                />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        <div className="donut-label">
          <strong>
            {Number(
              total
            ).toLocaleString()}
          </strong>

          <span>Students</span>
        </div>
      </div>

      <div className="legend-list">
        {data.map((item) => (
          <div
            className="legend-item"
            key={item.name}
          >
            <i
              style={{
                background:
                  item.color,
              }}
            />

            <span>
              {item.name}

              <b>
                {Number(
                  item.count
                ).toLocaleString()}
              </b>

              <small>
                ({item.value}%)
              </small>
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ============================================================
   TREND CHART
============================================================ */

function TrendChart({
  data,
}: {
  data?: any[]
}) {
  const chartData =
    data?.length
      ? data.map((item) => ({
          ...item,
          month: String(
            item.month
          ).slice(5),
        }))
      : fallbackTrendData

  return (
    <div className="trend-chart">
      <ResponsiveContainer
        width="100%"
        height="100%"
      >
        <RechartsLineChart
          data={chartData}
          margin={{
            left: -24,
            right: 4,
            top: 6,
            bottom: 0,
          }}
        >
          <CartesianGrid
            vertical={false}
            stroke="var(--border)"
          />

          <XAxis
            dataKey="month"
            tickLine={false}
            axisLine={false}
            tick={{
              fill:
                'var(--muted-foreground)',
              fontSize: 10,
            }}
          />

          <YAxis
            tickLine={false}
            axisLine={false}
            tick={{
              fill:
                'var(--muted-foreground)',
              fontSize: 10,
            }}
            domain={[0, 100]}
          />

          <Tooltip />

          <Line
            dataKey="low"
            stroke="var(--risk-low)"
            strokeWidth={2}
            dot={{ r: 2 }}
          />

          <Line
            dataKey="medium"
            stroke="var(--risk-medium)"
            strokeWidth={2}
            dot={{ r: 2 }}
          />

          <Line
            dataKey="high"
            stroke="var(--risk-high)"
            strokeWidth={2}
            dot={{ r: 2 }}
          />

          <Line
            dataKey="critical"
            stroke="var(--risk-critical)"
            strokeWidth={2}
            dot={{ r: 2 }}
          />
        </RechartsLineChart>
      </ResponsiveContainer>

      <div className="chart-legend">
        <span className="low">
          ● Low Risk
        </span>

        <span className="medium">
          ● Medium Risk
        </span>

        <span className="high">
          ● High Risk
        </span>

        <span className="critical">
          ● Critical Risk
        </span>
      </div>
    </div>
  )
}

/* ============================================================
   MAIN PAGE
============================================================ */

export default function Page() {
  const [active, setActive] =
    useState('Overview')

  const [
    openModule,
    setOpenModule,
  ] =
    useState<string | null>(null)

  const [
    sidebarOpen,
    setSidebarOpen,
  ] = useState(true)

  const [toast, setToast] =
    useState('')

  const [overview, setOverview] =
    useState<any>(null)

  const [
    factorData,
    setFactorData,
  ] = useState<any[]>([])

  const [
    apiConnected,
    setApiConnected,
  ] = useState(false)

  const notify = (
    message: string
  ) => {
    setToast(message)

    window.setTimeout(
      () => setToast(''),
      2200
    )
  }

  /* ==========================================================
     LOAD BACKEND DATA
  ========================================================== */

  useEffect(() => {
    Promise.all([
      vizApi.overview(),
      vizApi.factors(),
    ])
      .then(
        ([
          overviewResponse,
          factorResponse,
        ]) => {
          setOverview(
            overviewResponse
          )

          setFactorData(
            factorResponse?.factors ??
              []
          )

          setApiConnected(
            Boolean(
              overviewResponse
                ?.model_status
                ?.loaded
            )
          )
        }
      )
      .catch(() => {
        setApiConnected(false)
      })
  }, [])

  const summary =
    overview?.summary

  const risk =
    summary?.risk ?? {}

  const totalStudents =
    summary?.total_students ??
    200000

  const displayFactors =
    factorData.length
      ? factorData
          .slice(0, 5)
          .map(
            (
              item,
              index
            ) =>
              [
                String(
                  item.feature
                ).replaceAll(
                  '_',
                  ' '
                ),

                Number(
                  item.percent
                ),

                factorColors[
                  index %
                    factorColors.length
                ],
              ] as const
          )
      : fallbackFactors

  /* ==========================================================
     SIDEBAR HELPERS
  ========================================================== */

  const toggleModule = (
    label: string
  ) => {
    setOpenModule(
      (
        current
      ) =>
        current === label
          ? null
          : label
    )
  }

  /* ==========================================================
     PAGE
  ========================================================== */

  return (
    <main className="dashboard-shell">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside
        className={`sidebar ${
          sidebarOpen
            ? ''
            : 'collapsed'
        }`}
      >

        {/* BRAND */}

        <div className="brand">
          <a
            href="/"
            aria-label="VIZHIPPAAN dashboard home"
          >
            <img
              src={logo}
              alt="VIZHIPPAAN Child Education Risk Intelligence Platform"
            />
          </a>

          <button
            type="button"
            className="icon-button sidebar-toggle"
            onClick={() =>
              setSidebarOpen(false)
            }
            aria-label="Collapse navigation"
          >
            <PanelLeftClose
              size={17}
            />
          </button>
        </div>

        {/* NAVIGATION */}

        <nav aria-label="Primary navigation">

          {/* OVERVIEW */}

          <button
            type="button"
            className={`nav-item ${
              active === 'Overview'
                ? 'active'
                : ''
            }`}
            onClick={() => {
              setActive(
                'Overview'
              )

              setOpenModule(null)

              notify(
                'Overview selected'
              )
            }}
          >
            <LayoutDashboard
              size={17}
            />

            <span>
              Overview
            </span>
          </button>

          {/* MODULES */}

          {navigationModules.map(
            (module) => {
              const ModuleIcon =
                module.icon

              const isOpen =
                openModule ===
                module.label

              const hasActiveChild =
                module.items.some(
                  (item) =>
                    item.label ===
                    active
                )

              return (
                <div
                  key={
                    module.label
                  }
                  className="nav-module"
                >

                  {/* MODULE HEADER */}

                  <button
                    type="button"
                    className={`nav-item module-button ${
                      hasActiveChild
                        ? 'module-active'
                        : ''
                    }`}
                    onClick={() =>
                      toggleModule(
                        module.label
                      )
                    }
                  >
                    <ModuleIcon
                      size={17}
                    />

                    <span>
                      {module.label}
                    </span>

                    <ChevronDown
                      size={15}
                      className={`module-chevron ${
                        isOpen
                          ? 'module-chevron-open'
                          : ''
                      }`}
                    />
                  </button>

                  {/* CHILDREN */}

                  {isOpen && (
                    <div className="nav-submenu">
                      {module.items.map(
                        (item) => {
                          const ItemIcon =
                            item.icon

                          return (
                            <button
                              type="button"
                              key={
                                item.label
                              }
                              className={`nav-item nav-subitem ${
                                active ===
                                item.label
                                  ? 'active'
                                  : ''
                              }`}
                              onClick={() => {
                                setActive(
                                  item.label
                                )

                                notify(
                                  `${item.label} selected`
                                )
                              }}
                            >
                              <ItemIcon
                                size={15}
                              />

                              <span>
                                {
                                  item.label
                                }
                              </span>
                            </button>
                          )
                        }
                      )}
                    </div>
                  )}
                </div>
              )
            }
          )}
        </nav>

        {/* ADMIN */}

        <div className="admin-card">
          <div className="admin-avatar">
            <Users size={20} />
          </div>

          <div>
            <strong>
              Admin User
            </strong>

            <span>
              District Admin
            </span>
          </div>

          <ChevronDown
            size={15}
          />
        </div>
      </aside>

      {/* ======================================================
          MAIN AREA
      ====================================================== */}

      <div className="main-area">

        {/* TOP BAR */}

        <header className="topbar">
          <div className="welcome">

            <button
              type="button"
              className="mobile-menu icon-button"
              onClick={() =>
                setSidebarOpen(
                  !sidebarOpen
                )
              }
              aria-label="Toggle navigation"
            >
              <Menu size={20} />
            </button>

            <div>
              <h1>
                Welcome back,
                Admin!{' '}
                <span>👋</span>
              </h1>

              <p>
                Empowering every
                child to stay,
                learn and thrive.
              </p>
            </div>
          </div>

          <div className="top-actions">

            <button
              type="button"
              className="select-button"
            >
              Academic Year

              <strong>
                2025 - 2026
              </strong>

              <ChevronDown
                size={15}
              />
            </button>

            <button
              type="button"
              className="select-button"
            >
              District

              <strong>
                All Districts
              </strong>

              <ChevronDown
                size={15}
              />
            </button>

            <button
              type="button"
              className="notification icon-button"
              onClick={() =>
                notify(
                  'You have 3 new alerts'
                )
              }
              aria-label="Notifications"
            >
              <Bell size={20} />

              <b>3</b>
            </button>

            <button
              type="button"
              className="export-button"
              onClick={() =>
                notify(
                  'Report export started'
                )
              }
            >
              <Download
                size={16}
              />

              Export Report
            </button>
          </div>
        </header>

        {/* ====================================================
            DASHBOARD CONTENT
        ==================================================== */}

        <div className="content">

          {/* KPI CARDS */}

          <div className="metric-grid">

            <MetricCard
              icon={Users}
              label="Total Students"
              value={Number(
                totalStudents
              ).toLocaleString()}
              note={
                apiConnected
                  ? 'Live dataset'
                  : 'Backend fallback'
              }
              color="var(--risk-purple)"
              tone="var(--success)"
            />

            <MetricCard
              icon={ShieldCheck}
              label="Low Risk"
              value={Number(
                risk.Low?.count ??
                  98732
              ).toLocaleString()}
              note={`${
                risk.Low
                  ?.percent ??
                49.4
              }% of students`}
              color="var(--risk-low)"
              tone="var(--muted-foreground)"
            />

            <MetricCard
              icon={
                AlertTriangle
              }
              label="Medium Risk"
              value={Number(
                risk.Medium
                  ?.count ??
                  62415
              ).toLocaleString()}
              note={`${
                risk.Medium
                  ?.percent ??
                31.2
              }% of students`}
              color="var(--risk-medium)"
              tone="var(--muted-foreground)"
            />

            <MetricCard
              icon={
                AlertTriangle
              }
              label="High Risk"
              value={Number(
                risk.High?.count ??
                  28457
              ).toLocaleString()}
              note={`${
                risk.High
                  ?.percent ??
                14.2
              }% of students`}
              color="var(--risk-high)"
              tone="var(--muted-foreground)"
            />

            <MetricCard
              icon={
                AlertTriangle
              }
              label="Critical Risk"
              value={Number(
                risk.Critical
                  ?.count ??
                  10396
              ).toLocaleString()}
              note={`${
                risk.Critical
                  ?.percent ??
                5.2
              }% of students`}
              color="var(--risk-critical)"
              tone="var(--muted-foreground)"
            />
          </div>

          {/* ==================================================
              ROW ONE
          ================================================== */}

          <div className="grid-row row-one">

            <Card
              title="Risk Distribution"
              className="distribution-card"
            >
              <RiskDistribution
                summary={
                  summary
                }
              />
            </Card>

            <Card
              title="Risk Trend Over Time"
              className="trend-card"
            >
              <TrendChart
                data={
                  overview?.risk_trend
                }
              />
            </Card>

            <Card
              title="Top Risk Factors (Overall)"
              className="factors-card"
            >
              <div className="factor-list">
                {displayFactors.map(
                  ([
                    name,
                    value,
                    color,
                  ]) => (
                    <div
                      className="factor-row"
                      key={name}
                    >
                      <span>
                        {name}
                      </span>

                      <div className="factor-bar">
                        <i
                          style={{
                            width: `${value}%`,
                            background:
                              color,
                          }}
                        />
                      </div>

                      <b>
                        {value}%
                      </b>
                    </div>
                  )
                )}
              </div>

              <button
                type="button"
                className="outline-button"
                onClick={() =>
                  notify(
                    'Showing all risk factors'
                  )
                }
              >
                View All Factors

                <ArrowRight
                  size={15}
                />
              </button>
            </Card>
          </div>

          {/* ==================================================
              ROW TWO
          ================================================== */}

          <div className="grid-row row-two">

            {/* HEATMAP */}

            <Card
              title="District Risk Heatmap"
              className="heatmap-card"
            >
              <div className="map-placeholder">

                <div className="map-grid" />

                <div className="map-shape">
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                </div>

                <div className="map-controls">
                  <button
                    type="button"
                    onClick={() =>
                      notify(
                        'Map zoomed in'
                      )
                    }
                  >
                    +
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      notify(
                        'Map zoomed out'
                      )
                    }
                  >
                    −
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      notify(
                        'Map reset'
                      )
                    }
                  >
                    ⌗
                  </button>
                </div>

                <div className="map-key">
                  <strong>
                    Risk Level
                  </strong>

                  <span>
                    <i className="low-dot" />
                    Low
                  </span>

                  <span>
                    <i className="medium-dot" />
                    Medium
                  </span>

                  <span>
                    <i className="high-dot" />
                    High
                  </span>

                  <span>
                    <i className="critical-dot" />
                    Critical
                  </span>
                </div>
              </div>

              <button
                type="button"
                className="outline-button map-button"
                onClick={() =>
                  notify(
                    'Opening full district map'
                  )
                }
              >
                View Full Map
              </button>
            </Card>

            {/* INTERVENTION */}

            <Card
              title={
                <>
                  Intervention Impact{' '}
                  <em>
                    (Simulator
                    Preview)
                  </em>
                </>
              }
              className="intervention-card"
            >
              <div className="intervention-list">
                {[
                  [
                    'Scholarship Program',
                    '18.6%',
                  ],
                  [
                    'Counselling Support',
                    '14.2%',
                  ],
                  [
                    'Attendance Support',
                    '12.7%',
                  ],
                  [
                    'Free Meal Program',
                    '9.8%',
                  ],
                  [
                    'Remedial Classes',
                    '8.1%',
                  ],
                ].map(
                  (
                    [
                      name,
                      value,
                    ],
                    index
                  ) => (
                    <div
                      key={name}
                    >
                      <span>
                        <i
                          className={`impact-icon i-${index}`}
                        />

                        {name}
                      </span>

                      <b>
                        ↓ {value}
                      </b>
                    </div>
                  )
                )}
              </div>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  notify(
                    'Simulator ready'
                  )
                }
              >
                Run Simulator
              </button>
            </Card>

            {/* ALERTS */}

            <Card
              title="Alerts & Early Warnings"
              className="alerts-card"
              action={
                <button
                  type="button"
                  className="text-button"
                  onClick={() =>
                    notify(
                      'Showing all alerts'
                    )
                  }
                >
                  View All
                </button>
              }
            >
              <div className="alerts-list">

                <button
                  type="button"
                  className="alert alert-red"
                  onClick={() =>
                    notify(
                      '1,250 students moved to High Risk'
                    )
                  }
                >
                  <AlertTriangle
                    size={17}
                  />

                  <span>
                    <strong>
                      1,250
                      students moved
                      to High Risk
                    </strong>

                    <small>
                      in the last 7
                      days
                    </small>
                  </span>

                  <ChevronRight
                    size={16}
                  />
                </button>

                <button
                  type="button"
                  className="alert alert-orange"
                  onClick={() =>
                    notify(
                      '342 students at risk of dropout'
                    )
                  }
                >
                  <AlertTriangle
                    size={17}
                  />

                  <span>
                    <strong>
                      342 students
                      at risk of
                      dropout
                    </strong>

                    <small>
                      within next
                      30 days
                    </small>
                  </span>

                  <ChevronRight
                    size={16}
                  />
                </button>

                <button
                  type="button"
                  className="alert alert-yellow"
                  onClick={() =>
                    notify(
                      '5 schools require immediate attention'
                    )
                  }
                >
                  <Zap size={17} />

                  <span>
                    <strong>
                      5 schools
                      require
                      immediate
                      attention
                    </strong>

                    <small>
                      High risk
                      concentration
                      detected
                    </small>
                  </span>

                  <ChevronRight
                    size={16}
                  />
                </button>

                <button
                  type="button"
                  className="alert alert-blue"
                  onClick={() =>
                    notify(
                      'Data quality issues detected'
                    )
                  }
                >
                  <Database
                    size={17}
                  />

                  <span>
                    <strong>
                      Data quality
                      issues
                      detected
                    </strong>

                    <small>
                      3 datasets
                      need review
                    </small>
                  </span>

                  <ChevronRight
                    size={16}
                  />
                </button>
              </div>
            </Card>
          </div>

          {/* ==================================================
              ROW THREE
          ================================================== */}

          <div className="grid-row row-three">

            {/* OPPORTUNITY */}

            <Card
              title="Opportunity Detector"
              className="utility-card opportunity"
            >
              <div className="opportunity-body">

                <div className="progress-ring">
                  <svg viewBox="0 0 42 42">
                    <circle
                      cx="21"
                      cy="21"
                      r="15.9"
                    />

                    <circle
                      className="progress"
                      cx="21"
                      cy="21"
                      r="15.9"
                    />
                  </svg>

                  <strong>
                    72%
                  </strong>

                  <span>
                    High Potential
                  </span>
                </div>

                <p>
                  <b>
                    14,856
                    students
                  </b>{' '}
                  can significantly
                  improve with right
                  support
                </p>
              </div>

              <button
                type="button"
                className="outline-button"
                onClick={() =>
                  notify(
                    'Showing opportunities'
                  )
                }
              >
                View Opportunities
              </button>
            </Card>

            {/* FAIRNESS */}

            <Card
              title="AI Fairness Auditor"
              className="utility-card"
            >
              <div className="audit-stat">
                <span>
                  Gender Parity
                  Difference
                </span>

                <b>
                  2.6%{' '}
                  <em>
                    (Good)
                  </em>
                </b>

                <CheckCircle2
                  size={20}
                />
              </div>

              <div className="audit-stat bottom">
                <span>
                  Groups Monitored
                </span>

                <b>
                  <Users
                    size={16}
                  />{' '}
                  6
                </b>
              </div>

              <button
                type="button"
                className="outline-button"
                onClick={() =>
                  notify(
                    'Opening fairness report'
                  )
                }
              >
                View Report
              </button>
            </Card>

            {/* RESOURCE ALLOCATION */}

            <Card
              title={
                <>
                  Resource
                  Allocation{' '}
                  <em>
                    (AI Optimizer)
                  </em>
                </>
              }
              className="utility-card resource"
            >
              <p className="small-heading">
                Optimal Allocation
                Suggestion
              </p>

              <div className="resource-grid">

                <div>
                  <GraduationCap
                    size={17}
                  />

                  <span>
                    Scholarships
                  </span>

                  <b>2,450</b>
                </div>

                <div>
                  <Users
                    size={17}
                  />

                  <span>
                    Counsellors
                  </span>

                  <b>120</b>
                </div>

                <div>
                  <PackageOpen
                    size={17}
                  />

                  <span>
                    Devices
                  </span>

                  <b>1,820</b>
                </div>

                <div>
                  <HandCoins
                    size={17}
                  />

                  <span>
                    Meals
                  </span>

                  <b>5,600</b>
                </div>
              </div>

              <button
                type="button"
                className="outline-button"
                onClick={() =>
                  notify(
                    'Opening allocation plan'
                  )
                }
              >
                View Allocation
                Plan
              </button>
            </Card>

            {/* SYSTEM */}

            <Card
              title="System Health"
              className="utility-card health"
            >
              <div className="health-list">

                <div>
                  <span>
                    <CheckCircle2
                      size={15}
                    />{' '}
                    Model Status
                  </span>

                  <b
                    className={
                      overview
                        ?.model_status
                        ?.loaded
                        ? 'healthy'
                        : ''
                    }
                  >
                    {overview
                      ?.model_status
                      ?.loaded
                      ? 'Healthy'
                      : 'Offline'}
                  </b>
                </div>

                <div>
                  <span>
                    <CheckCircle2
                      size={15}
                    />{' '}
                    API Status
                  </span>

                  <b
                    className={
                      apiConnected
                        ? 'healthy'
                        : ''
                    }
                  >
                    {apiConnected
                      ? 'Healthy'
                      : 'Offline'}
                  </b>
                </div>

                <div>
                  <span>
                    <Database
                      size={15}
                    />{' '}
                    Data Pipeline
                  </span>

                  <b
                    className={
                      summary
                        ? 'healthy'
                        : ''
                    }
                  >
                    {summary
                      ? 'Healthy'
                      : 'Offline'}
                  </b>
                </div>

                <div>
                  <span>
                    <Clock3
                      size={15}
                    />{' '}
                    Last Updated
                  </span>

                  <b>
                    {apiConnected
                      ? 'Live'
                      : 'Waiting'}
                  </b>
                </div>
              </div>

              <button
                type="button"
                className="outline-button"
                onClick={() =>
                  notify(
                    'Opening system dashboard'
                  )
                }
              >
                System Dashboard
              </button>
            </Card>
          </div>
        </div>

        {/* ====================================================
            FOOTER
        ==================================================== */}

        <footer>
          <span>
            <span className="heart">
              ♥
            </span>{' '}
            Every child has
            potential. VIZHIPPAAN
            ensures no child is
            left behind.
          </span>

          <span>
            VIZHIPPAAN © 2026
            <i />
            AI for Social Good
          </span>
        </footer>
      </div>

      {/* ======================================================
          TOAST
      ====================================================== */}

      {toast && (
        <div className="toast">
          <CheckCircle2
            size={16}
          />

          {toast}
        </div>
      )}
    </main>
  )
}
