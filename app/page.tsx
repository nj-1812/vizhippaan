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
  Sparkles,
  Target,
  Users,
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
   TYPES
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

type FeaturePageProps = {
  title: string
  description: string
  icon: ElementType
  children?: ReactNode
}

/* ============================================================
   SIDEBAR MODULES
============================================================ */

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
  { month: 'Jan', low: 58, medium: 34, high: 14, critical: 3 },
  { month: 'Feb', low: 64, medium: 31, high: 16, critical: 3 },
  { month: 'Mar', low: 56, medium: 34, high: 13, critical: 3 },
  { month: 'Apr', low: 59, medium: 32, high: 12, critical: 3 },
  { month: 'May', low: 61, medium: 30, high: 11, critical: 3 },
  { month: 'Jun', low: 65, medium: 32, high: 9, critical: 3 },
  { month: 'Jul', low: 60, medium: 30, high: 12, critical: 3 },
  { month: 'Aug', low: 61, medium: 31, high: 12, critical: 3 },
  { month: 'Sep', low: 60, medium: 31, high: 13, critical: 3 },
  { month: 'Oct', low: 64, medium: 29, high: 11, critical: 3 },
  { month: 'Nov', low: 60, medium: 29, high: 12, critical: 3 },
  { month: 'Dec', low: 54, medium: 30, high: 12, critical: 3 },
]

const fallbackFactors = [
  ['Low Attendance', 42, 'var(--risk-critical)'],
  ['Low Test Scores', 37, 'var(--risk-blue)'],
  ['Low Household Income', 31, 'var(--risk-teal)'],
  ['Large Distance to School', 22, 'var(--risk-purple)'],
  ['No Internet Access', 19, 'var(--risk-pink)'],
] as const

const factorColors = [
  'var(--risk-critical)',
  'var(--risk-blue)',
  'var(--risk-teal)',
  'var(--risk-purple)',
  'var(--risk-pink)',
]

const spark = [2, 4, 3, 6, 4, 7, 5, 8, 6, 9, 7, 10]

/* ============================================================
   MINI SPARK
============================================================ */

function MiniSpark({
  color,
}: {
  color: string
}) {
  const data = spark.map((value, index) => ({
    index,
    value,
  }))

  return (
    <ResponsiveContainer width="100%" height="100%">
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
   GENERIC CARD
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
    <section className={`panel ${className}`}>
      <div className="panel-heading">
        <h2>{title}</h2>
        {action}
      </div>

      {children}
    </section>
  )
}

/* ============================================================
   FEATURE PAGE
============================================================ */

function FeaturePage({
  title,
  description,
  icon: Icon,
  children,
}: FeaturePageProps) {
  return (
    <section className="feature-page">
      <div className="feature-page-header">
        <div className="feature-page-icon">
          <Icon size={24} />
        </div>

        <div>
          <h1>{title}</h1>
          <p>{description}</p>
        </div>
      </div>

      <div className="feature-page-content">
        {children ?? (
          <section className="panel feature-placeholder">
            <Icon size={34} />

            <h2>{title}</h2>

            <p>
              This intelligence workspace is ready for its live
              VIZHIPPAAN backend feature integration.
            </p>
          </section>
        )}
      </div>
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
      value: risk.Low?.percent ?? 49.4,
      count: risk.Low?.count ?? 98732,
      color: 'var(--risk-low)',
    },
    {
      name: 'Medium Risk',
      value: risk.Medium?.percent ?? 31.2,
      count: risk.Medium?.count ?? 62415,
      color: 'var(--risk-medium)',
    },
    {
      name: 'High Risk',
      value: risk.High?.percent ?? 14.2,
      count: risk.High?.count ?? 28457,
      color: 'var(--risk-high)',
    },
    {
      name: 'Critical Risk',
      value: risk.Critical?.percent ?? 5.2,
      count: risk.Critical?.count ?? 10396,
      color: 'var(--risk-critical)',
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
            {Number(total).toLocaleString()}
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
                background: item.color,
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
   TREND
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
              fill: 'var(--muted-foreground)',
              fontSize: 10,
            }}
          />

          <YAxis
            tickLine={false}
            axisLine={false}
            tick={{
              fill: 'var(--muted-foreground)',
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
  ] =
    useState<any[]>([])

  const [
    apiConnected,
    setApiConnected,
  ] = useState(false)

  /* ==========================================================
     TOAST
  ========================================================== */

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
     API DATA
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

  /* ==========================================================
     DATA
  ========================================================== */

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
      (current) =>
        current === label
          ? null
          : label
    )
  }

  const selectFeature = (
    label: string
  ) => {
    setActive(label)

    notify(
      `${label} selected`
    )
  }

  /* ==========================================================
     OVERVIEW
  ========================================================== */

  const renderOverview = () => (
    <>
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
            risk.Low?.percent ??
            49.4
          }% of students`}
          color="var(--risk-low)"
          tone="var(--muted-foreground)"
        />

        <MetricCard
          icon={AlertTriangle}
          label="Medium Risk"
          value={Number(
            risk.Medium?.count ??
              62415
          ).toLocaleString()}
          note={`${
            risk.Medium?.percent ??
            31.2
          }% of students`}
          color="var(--risk-medium)"
          tone="var(--muted-foreground)"
        />

        <MetricCard
          icon={AlertTriangle}
          label="High Risk"
          value={Number(
            risk.High?.count ??
              28457
          ).toLocaleString()}
          note={`${
            risk.High?.percent ??
            14.2
          }% of students`}
          color="var(--risk-high)"
          tone="var(--muted-foreground)"
        />

        <MetricCard
          icon={AlertTriangle}
          label="Critical Risk"
          value={Number(
            risk.Critical?.count ??
              10396
          ).toLocaleString()}
          note={`${
            risk.Critical?.percent ??
            5.2
          }% of students`}
          color="var(--risk-critical)"
          tone="var(--muted-foreground)"
        />
      </div>

      <div className="grid-row row-one">
        <Card
          title="Risk Distribution"
          className="distribution-card"
        >
          <RiskDistribution
            summary={summary}
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
    </>
  )

  /* ==========================================================
     HEATMAP
  ========================================================== */

  const renderHeatmap = () => (
    <FeaturePage
      title="GIS Educational Risk Heatmap"
      description="Explore dropout-risk concentration geographically across districts, blocks, villages and schools."
      icon={Map}
    >
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
      </Card>
    </FeaturePage>
  )

  /* ==========================================================
     INTERVENTION SIMULATOR
  ========================================================== */

  const renderInterventionSimulator = () => (
    <FeaturePage
      title="Intervention Impact Simulator"
      description="Compare support strategies and estimate how individual interventions could reduce student dropout risk."
      icon={CircleDollarSign}
    >
      <div className="grid-row row-two">
        <Card
          title={
            <>
              Intervention Impact{' '}
              <em>
                Simulator
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
                'Intervention simulation started'
              )
            }
          >
            Run Simulator
          </button>
        </Card>

        <Card title="Simulation Guidance">
          <div className="feature-info-list">
            <div>
              <strong>
                Attendance Improvement
              </strong>

              <span>
                Model the effect of improved regular attendance.
              </span>
            </div>

            <div>
              <strong>
                Financial Support
              </strong>

              <span>
                Test scholarship and welfare assistance scenarios.
              </span>
            </div>

            <div>
              <strong>
                Transport Support
              </strong>

              <span>
                Estimate impact of reducing commute barriers.
              </span>
            </div>

            <div>
              <strong>
                Counselling
              </strong>

              <span>
                Simulate behavioural and mentoring interventions.
              </span>
            </div>
          </div>
        </Card>
      </div>
    </FeaturePage>
  )

  /* ==========================================================
     RESOURCE ALLOCATION
  ========================================================== */

  const renderResourceAllocation = () => (
    <FeaturePage
      title="AI Resource Allocation Optimizer"
      description="Optimize scholarships, counsellors, devices, meals and support resources for maximum educational impact."
      icon={HandCoins}
    >
      <Card
        title={
          <>
            Optimal Allocation{' '}
            <em>
              AI Optimizer
            </em>
          </>
        }
        className="resource"
      >
        <div className="resource-grid">
          <div>
            <GraduationCap
              size={18}
            />

            <span>
              Scholarships
            </span>

            <b>
              2,450
            </b>
          </div>

          <div>
            <Users size={18} />

            <span>
              Counsellors
            </span>

            <b>
              120
            </b>
          </div>

          <div>
            <PackageOpen
              size={18}
            />

            <span>
              Devices
            </span>

            <b>
              1,820
            </b>
          </div>

          <div>
            <HandCoins
              size={18}
            />

            <span>
              Meals
            </span>

            <b>
              5,600
            </b>
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
          View Allocation Plan
        </button>
      </Card>
    </FeaturePage>
  )

  /* ==========================================================
     OPPORTUNITY
  ========================================================== */

  const renderOpportunityDetector = () => (
    <FeaturePage
      title="Opportunity Detector"
      description="Detect students who could improve significantly with timely and appropriate support."
      icon={Lightbulb}
    >
      <Card
        title="Opportunity Intelligence"
        className="opportunity"
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
              14,856 students
            </b>{' '}
            can significantly improve with targeted support.
          </p>
        </div>

        <button
          type="button"
          className="outline-button"
          onClick={() =>
            notify(
              'Showing opportunity candidates'
            )
          }
        >
          View Opportunities
        </button>
      </Card>
    </FeaturePage>
  )

  /* ==========================================================
     FAIRNESS
  ========================================================== */

  const renderFairnessAuditor = () => (
    <FeaturePage
      title="AI Fairness Auditor"
      description="Evaluate model outcomes across student groups and monitor potential algorithmic bias."
      icon={ShieldCheck}
    >
      <div className="grid-row row-two">
        <Card title="Gender Parity">
          <div className="audit-stat">
            <span>
              Gender Parity Difference
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
        </Card>

        <Card title="Groups Monitored">
          <div className="audit-stat bottom">
            <span>
              Protected / Comparison Groups
            </span>

            <b>
              <Users
                size={16}
              />{' '}
              6
            </b>
          </div>
        </Card>
      </div>
    </FeaturePage>
  )

  /* ==========================================================
     QUALITY GUARDIAN
  ========================================================== */

  const renderQualityGuardian = () => (
    <FeaturePage
      title="App Quality Guardian"
      description="Monitor model health, API availability, data pipelines and operational reliability."
      icon={HeartPulse}
    >
      <Card
        title="System Health"
        className="health"
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
      </Card>
    </FeaturePage>
  )

  /* ==========================================================
     ACTIVE CONTENT
  ========================================================== */

  const renderActiveContent = () => {
    switch (active) {
      case 'Overview':
        return renderOverview()

      case 'AI Student Digital Twin':
        return (
          <FeaturePage
            title="AI Student Digital Twin"
            description="Live student intelligence profile combining academic, attendance, behavioural and socioeconomic indicators."
            icon={Bot}
          />
        )

      case 'Student Journey Timeline':
        return (
          <FeaturePage
            title="Student Journey Timeline"
            description="Follow each student's educational journey, risk progression, interventions and important milestones over time."
            icon={Clock3}
          />
        )

      case 'Risk Explanation':
        return (
          <FeaturePage
            title="Explainable Risk Intelligence"
            description="Understand the precise factors contributing to each AI risk prediction using explainability insights."
            icon={Info}
          />
        )

      case 'Early Warning Horizon':
        return (
          <FeaturePage
            title="Early Warning Horizon"
            description="Forecast likely student-risk movement across future 30-day, 60-day, 90-day and longer horizons."
            icon={Target}
          />
        )

      case 'AI Root Cause Graph':
        return (
          <FeaturePage
            title="AI Root Cause Graph"
            description="Visualize relationships such as financial hardship → transport barriers → absenteeism → educational disengagement."
            icon={Network}
          />
        )

      case 'Future School Simulator':
        return (
          <FeaturePage
            title="Future School Simulator"
            description="Model future school-level outcomes under different attendance, academic, resource and intervention scenarios."
            icon={Building2}
          />
        )

      case 'Opportunity Detector':
        return renderOpportunityDetector()

      case 'Intervention Simulator':
        return renderInterventionSimulator()

      case 'Resource Allocation':
        return renderResourceAllocation()

      case 'Intervention Marketplace':
        return (
          <FeaturePage
            title="Intervention Marketplace"
            description="Browse intervention options with estimated costs, target groups, expected success and implementation priority."
            icon={ShoppingCart}
          />
        )

      case 'AI Policy Simulator':
        return (
          <FeaturePage
            title="AI Policy Simulator"
            description="Estimate potential outcomes of educational policies before district or state-level deployment."
            icon={Landmark}
          />
        )

      case 'Heatmap':
        return renderHeatmap()

      case 'AI Fairness Auditor':
        return renderFairnessAuditor()

      case 'Multi-Agent Council':
        return (
          <FeaturePage
            title="Multi-Agent Council"
            description="Multiple specialized AI reasoning agents collaboratively evaluate student risk, intervention and policy decisions."
            icon={BrainCircuit}
          />
        )

      case 'App Quality Guardian':
        return renderQualityGuardian()

      default:
        return (
          <FeaturePage
            title={active}
            description="VIZHIPPAAN intelligence workspace."
            icon={Sparkles}
          />
        )
    }
  }

  /* ==========================================================
     PAGE
  ========================================================== */

  return (
    <main className="dashboard-shell">

      {/* SIDEBAR */}

      <aside
        className={`sidebar ${
          sidebarOpen
            ? ''
            : 'collapsed'
        }`}
      >
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

        <nav aria-label="Primary navigation">

          <button
            type="button"
            className={`nav-item ${
              active === 'Overview'
                ? 'active'
                : ''
            }`}
            onClick={() => {
              setActive('Overview')
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
                              onClick={() =>
                                selectFeature(
                                  item.label
                                )
                              }
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

      {/* MAIN */}

      <div className="main-area">

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
                {active === 'Overview'
                  ? 'Welcome back, Admin!'
                  : active}{' '}

                {active === 'Overview' && (
                  <span>
                    👋
                  </span>
                )}
              </h1>

              <p>
                {active === 'Overview'
                  ? 'Empowering every child to stay, learn and thrive.'
                  : 'VIZHIPPAAN Intelligence Workspace'}
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

              <b>
                3
              </b>
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

        {/* IMPORTANT FIX:
            Overview gets fullscreen-fit CSS.
            Feature pages get their own scrolling area.
        */}

        <div
          className={`content ${
            active === 'Overview'
              ? 'overview-content'
              : 'feature-content'
          }`}
        >
          {renderActiveContent()}
        </div>

        <footer>
          <span>
            <span className="heart">
              ♥
            </span>{' '}

            Every child has potential.
            VIZHIPPAAN ensures no child is left behind.
          </span>

          <span>
            VIZHIPPAAN © 2026

            <i />

            AI for Social Good
          </span>
        </footer>
      </div>

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
