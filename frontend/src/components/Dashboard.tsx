import React from 'react';
import { Row, Col, Card, Container, OverlayTrigger, Tooltip as BSTooltip } from 'react-bootstrap';
import { FaMoneyBillWave, FaCalendarDay, FaTags, FaChartLine, FaReceipt, FaCrown } from 'react-icons/fa';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import { DashboardStats } from '../types';

interface DashboardProps {
  stats: DashboardStats | null;
}

const CHART_COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#8b5cf6', '#06b6d4', '#84cc16'];

export const Dashboard: React.FC<DashboardProps> = ({ stats }) => {
  if (!stats) {
    return (
      <Container fluid className="py-5">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading dashboard analytics...</p>
        </div>
      </Container>
    );
  }

  // Prepare data for pie chart
  const pieChartData = stats?.category_distribution?.map((item, index) => ({
    ...item,
    fill: CHART_COLORS[index % CHART_COLORS.length]
  })) || [];

  return (
    <Container fluid className="py-4">
      {/* Main KPI Cards */}
      <Row className="mb-5">
        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="total-spending-tooltip">
                Total amount spent across all categories this month. This includes all your recorded transactions.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaMoneyBillWave className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Monthly Total</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  ${stats?.total_spending?.toFixed(2) || '0.00'}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>

        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="daily-average-tooltip">
                Average amount you spend per day based on your monthly spending patterns.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaCalendarDay className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Daily Average</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  ${stats?.average_daily?.toFixed(2) || '0.00'}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>

        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="weekly-total-tooltip">
                Total amount spent in the current week. This helps track weekly spending patterns.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaChartLine className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Weekly Total</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  ${stats?.weekly_spending?.toFixed(2) || '0.00'}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>

        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="transactions-tooltip">
                Total number of spending transactions recorded this month.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaReceipt className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Transactions</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  {stats?.monthly_transactions || 0}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>

        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="highest-spend-tooltip">
                The largest single transaction amount recorded this month.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaCrown className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Highest Spend</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  ${stats?.highest_single_spending?.toFixed(2) || '0.00'}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>

        <Col xl={2} lg={3} md={4} sm={6} className="mb-4">
          <OverlayTrigger
            placement="top"
            overlay={
              <BSTooltip id="categories-tooltip">
                Number of different spending categories you've used this month.
              </BSTooltip>
            }
          >
            <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', cursor: 'help' }}>
              <Card.Body className="text-center text-white p-4">
                <FaTags className="mb-3" size={32} />
                <Card.Title className="h6 mb-2">Categories</Card.Title>
                <Card.Text className="h4 mb-0 fw-bold">
                  {stats?.category_distribution?.length || 0}
                </Card.Text>
              </Card.Body>
            </Card>
          </OverlayTrigger>
        </Col>
      </Row>

      {/* Charts Section */}
      <Row className="mb-5">
        <Col lg={8} className="mb-4">
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-white border-0 py-4">
              <div className="d-flex align-items-center">
                <OverlayTrigger
                  placement="top"
                  overlay={
                    <BSTooltip id="trend-tooltip">
                      This chart shows your daily spending patterns over the past week, helping you identify spending trends and patterns.
                    </BSTooltip>
                  }
                >
                  <FaChartLine className="text-primary me-3" size={24} style={{ cursor: 'help' }} />
                </OverlayTrigger>
                <h5 className="mb-0 fw-bold">Weekly Spending Trend</h5>
              </div>
            </Card.Header>
            <Card.Body className="p-4">
              {stats.weekly_trend && stats.weekly_trend.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={stats.weekly_trend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis 
                      dataKey="date" 
                      stroke="#666"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#666"
                      fontSize={12}
                      tickFormatter={(value) => `$${value}`}
                    />
                    
                    <Tooltip 
                      formatter={(value) => [`$${value}`, 'Spending']}
                      labelStyle={{ color: '#333' }}
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #ddd',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="amount" 
                      stroke="#4f46e5" 
                      strokeWidth={3}
                      dot={{ fill: '#4f46e5', r: 6 }}
                      activeDot={{ r: 8, stroke: '#4f46e5', strokeWidth: 2 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center text-muted py-5">
                  <FaChartLine size={48} className="mb-3 opacity-50" />
                  <p className="h6">No trend data available</p>
                  <p className="small">Add more expenses to see weekly trends</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4} className="mb-4">
          <Card className="border-0 shadow-sm h-100">
            <Card.Header className="bg-white border-0 py-4">
              <div className="d-flex align-items-center">
                <OverlayTrigger
                  placement="top"
                  overlay={
                    <BSTooltip id="category-tooltip">
                      This pie chart shows how your spending is distributed across different categories, helping you understand where most of your money goes.
                    </BSTooltip>
                  }
                >
                  <FaTags className="text-success me-3" size={24} style={{ cursor: 'help' }} />
                </OverlayTrigger>
                <h5 className="mb-0 fw-bold">Category Distribution</h5>
              </div>
            </Card.Header>
            <Card.Body className="p-4">
              {stats.category_distribution && stats.category_distribution.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieChartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={80}
                      paddingAngle={2}
                      dataKey="amount"
                      nameKey="category"
                      label={({ category, percent }) => 
                        percent && percent > 0.05 ? `${category} (${(percent * 100).toFixed(0)}%)` : ''
                      }
                      labelLine={false}
                    >
                      {pieChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value, name) => [`$${Number(value).toFixed(2)}`, 'Amount']}
                      labelFormatter={(label) => `Category: ${label}`}
                      contentStyle={{ 
                        backgroundColor: '#fff', 
                        border: '1px solid #ddd',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                      }}
                    />
                    <Legend 
                      verticalAlign="bottom" 
                      height={36}
                      formatter={(value) => value}
                      iconType="circle"
                    />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center text-muted py-5">
                  <FaTags size={48} className="mb-3 opacity-50" />
                  <p className="h6">No spending data available</p>
                  <p className="small">Add some expenses to see category distribution</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Top Categories List */}
      <Row>
        <Col lg={12}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white border-0 py-4">
              <div className="d-flex align-items-center">
                <OverlayTrigger
                  placement="top"
                  overlay={
                    <BSTooltip id="top-categories-tooltip">
                      This section shows your top spending categories ranked by total amount spent this month.
                    </BSTooltip>
                  }
                >
                  <FaTags className="text-warning me-3" size={24} style={{ cursor: 'help' }} />
                </OverlayTrigger>
                <h5 className="mb-0 fw-bold">Top Spending Categories This Month</h5>
              </div>
            </Card.Header>
            <Card.Body className="p-4">
              <Row>
                {(stats?.top_categories || []).map((cat, idx) => (
                  <Col md={6} lg={4} xl={2} key={cat.category} className="mb-3">
                    <div className="d-flex align-items-center p-3 bg-light rounded-3">
                      <div 
                        className="rounded-circle me-3 d-flex align-items-center justify-content-center text-white fw-bold"
                        style={{ 
                          width: '40px', 
                          height: '40px', 
                          backgroundColor: CHART_COLORS[idx % CHART_COLORS.length],
                          fontSize: '14px'
                        }}
                      >
                        #{idx + 1}
                      </div>
                      <div className="flex-grow-1">
                        <div className="fw-bold text-dark">{cat.category}</div>
                        <div className="text-success fw-bold">${cat.amount.toFixed(2)}</div>
                      </div>
                    </div>
                  </Col>
                ))}
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};
