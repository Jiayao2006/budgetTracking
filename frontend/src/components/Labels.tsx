import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Container, Button, Modal, OverlayTrigger, Tooltip as BSTooltip } from 'react-bootstrap';
import { FaTag, FaMoneyBillWave, FaCalendarDay, FaReceipt, FaChartLine, FaEye } from 'react-icons/fa';
import { LabelsOverview, LabelStats } from '../types';
import { useAuth } from '../context/AuthContext';
import { formatCurrency } from '../utils/currencyFormat';

const CARD_COLORS = [
  'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
  'linear-gradient(135deg, #10b981 0%, #059669 100%)',
  'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
  'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
  'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
  'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
  'linear-gradient(135deg, #84cc16 0%, #65a30d 100%)',
  'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',
];

export const Labels: React.FC = () => {
  const { user } = useAuth();
  const preferredCurrency = user?.preferred_currency || 'USD';
  const [labelsOverview, setLabelsOverview] = useState<LabelsOverview | null>(null);
  const [selectedLabel, setSelectedLabel] = useState<LabelStats | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLabelsOverview();
  }, []);

  const fetchLabelsOverview = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch('/api/labels/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch labels: ${response.statusText}`);
      }

      const data: LabelsOverview = await response.json();
      setLabelsOverview(data);
    } catch (error) {
      console.error('Error fetching labels overview:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch labels');
    } finally {
      setLoading(false);
    }
  };

  const fetchLabelDetails = async (labelName: string) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`/api/labels/${encodeURIComponent(labelName)}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch label details: ${response.statusText}`);
      }

      const data: LabelStats = await response.json();
      setSelectedLabel(data);
      setShowDetailModal(true);
    } catch (error) {
      console.error('Error fetching label details:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch label details');
    }
  };

  if (loading) {
    return (
      <Container fluid className="py-5">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading labels analytics...</p>
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container fluid className="py-5">
        <div className="text-center">
          <div className="alert alert-danger" role="alert">
            <FaTag className="me-2" />
            Error: {error}
          </div>
          <Button variant="primary" onClick={fetchLabelsOverview}>
            Try Again
          </Button>
        </div>
      </Container>
    );
  }

  if (!labelsOverview || labelsOverview.labels_stats.length === 0) {
    return (
      <Container fluid className="py-5">
        <div className="text-center">
          <FaTag className="text-muted mb-3" size={48} />
          <h4 className="text-muted">No Labels Found</h4>
          <p className="text-muted">
            Start adding labels to your spendings to see analytics here!
          </p>
        </div>
      </Container>
    );
  }

  return (
    <Container fluid className="py-4">
      {/* Header */}
      <Row className="mb-4">
        <Col>
          <div className="d-flex align-items-center mb-3">
            <FaTag className="text-primary me-3" size={32} />
            <div>
              <h2 className="mb-1">Spending Labels</h2>
              <p className="text-muted mb-0">
                Track and analyze your spending by custom labels
              </p>
            </div>
          </div>
        </Col>
      </Row>

      {/* Overview Stats */}
      <Row className="mb-5">
        <Col xl={3} lg={4} md={6} className="mb-4">
          <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)' }}>
            <Card.Body className="text-center text-white p-4">
              <FaTag className="mb-3" size={32} />
              <Card.Title className="h6 mb-2">Total Labels</Card.Title>
              <Card.Text className="h4 mb-0 fw-bold">
                {labelsOverview.total_labels}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col xl={3} lg={4} md={6} className="mb-4">
          <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
            <Card.Body className="text-center text-white p-4">
              <FaMoneyBillWave className="mb-3" size={32} />
              <Card.Title className="h6 mb-2">Total Labeled Spending</Card.Title>
              <Card.Text className="h4 mb-0 fw-bold">
                {formatCurrency(
                  labelsOverview.labels_stats.reduce((total, label) => total + label.total_spending, 0),
                  preferredCurrency
                )}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col xl={3} lg={4} md={6} className="mb-4">
          <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)' }}>
            <Card.Body className="text-center text-white p-4">
              <FaReceipt className="mb-3" size={32} />
              <Card.Title className="h6 mb-2">Labeled Transactions</Card.Title>
              <Card.Text className="h4 mb-0 fw-bold">
                {labelsOverview.labels_stats.reduce((total, label) => total + label.transaction_count, 0)}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col xl={3} lg={4} md={6} className="mb-4">
          <Card className="h-100 border-0 shadow-sm" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }}>
            <Card.Body className="text-center text-white p-4">
              <FaChartLine className="mb-3" size={32} />
              <Card.Title className="h6 mb-2">Average per Label</Card.Title>
              <Card.Text className="h4 mb-0 fw-bold">
                {formatCurrency(
                  labelsOverview.labels_stats.reduce((total, label) => total + label.total_spending, 0) / labelsOverview.total_labels,
                  preferredCurrency
                )}
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Individual Label Cards */}
      <Row className="mb-4">
        <Col>
          <h4 className="mb-3">
            <FaTag className="text-primary me-2" />
            Your Labels
          </h4>
        </Col>
      </Row>

      <Row>
        {labelsOverview.labels_stats.map((label: LabelStats, index: number) => (
          <Col xl={3} lg={4} md={6} className="mb-4" key={label.label}>
            <Card className="h-100 border-0 shadow-sm position-relative overflow-hidden">
              <div 
                className="position-absolute top-0 start-0 w-100 h-1"
                style={{ background: CARD_COLORS[index % CARD_COLORS.length] }}
              />
              <Card.Body className="p-4">
                <div className="d-flex justify-content-between align-items-start mb-3">
                  <div className="flex-grow-1">
                    <Card.Title className="h6 mb-1 text-truncate" title={label.label}>
                      {label.label}
                    </Card.Title>
                    <Card.Text className="text-muted small mb-0">
                      {label.transaction_count} transaction{label.transaction_count !== 1 ? 's' : ''}
                    </Card.Text>
                  </div>
                  <OverlayTrigger
                    placement="top"
                    overlay={
                      <BSTooltip id={`view-details-${index}`}>
                        View detailed analytics for this label
                      </BSTooltip>
                    }
                  >
                    <Button
                      variant="link"
                      size="sm"
                      className="p-1 text-primary"
                      onClick={() => fetchLabelDetails(label.label)}
                    >
                      <FaEye />
                    </Button>
                  </OverlayTrigger>
                </div>

                <div className="mb-3">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small">Total Spending</span>
                    <span className="fw-bold text-secondary">
                      {formatCurrency(label.total_spending, preferredCurrency)}
                    </span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small">Average</span>
                    <span className="text-secondary">
                      {formatCurrency(label.average_per_transaction, preferredCurrency)}
                    </span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center">
                    <span className="text-muted small">Highest Spend</span>
                    <span className="text-secondary">
                      {formatCurrency(label.highest_spending_amount, preferredCurrency)}
                    </span>
                  </div>
                </div>

                {label.highest_spending_date && (
                  <div className="text-center">
                    <small className="text-muted">
                      Highest spend on {new Date(label.highest_spending_date).toLocaleDateString()}
                    </small>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Detail Modal */}
      <Modal show={showDetailModal} onHide={() => setShowDetailModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            <FaTag className="me-2 text-primary" />
            {selectedLabel?.label} - Detailed Analytics
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedLabel && (
            <Row>
              <Col md={6} className="mb-3">
                <Card className="border-0 bg-light">
                  <Card.Body className="text-center">
                    <FaMoneyBillWave className="text-primary mb-2" size={24} />
                    <h6 className="mb-1">Total Spending</h6>
                    <h4 className="text-primary mb-0">
                      {formatCurrency(selectedLabel.total_spending, preferredCurrency)}
                    </h4>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={6} className="mb-3">
                <Card className="border-0 bg-light">
                  <Card.Body className="text-center">
                    <FaReceipt className="text-success mb-2" size={24} />
                    <h6 className="mb-1">Transactions</h6>
                    <h4 className="text-success mb-0">
                      {selectedLabel.transaction_count}
                    </h4>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={6} className="mb-3">
                <Card className="border-0 bg-light">
                  <Card.Body className="text-center">
                    <FaChartLine className="text-info mb-2" size={24} />
                    <h6 className="mb-1">Average per Transaction</h6>
                    <h4 className="text-info mb-0">
                      {formatCurrency(selectedLabel.average_per_transaction, preferredCurrency)}
                    </h4>
                  </Card.Body>
                </Card>
              </Col>
              <Col md={6} className="mb-3">
                <Card className="border-0 bg-light">
                  <Card.Body className="text-center">
                    <FaCalendarDay className="text-warning mb-2" size={24} />
                    <h6 className="mb-1">Highest Single Spend</h6>
                    <h4 className="text-warning mb-0">
                      {formatCurrency(selectedLabel.highest_spending_amount, preferredCurrency)}
                    </h4>
                    {selectedLabel.highest_spending_date && (
                      <small className="text-muted">
                        on {new Date(selectedLabel.highest_spending_date).toLocaleDateString()}
                      </small>
                    )}
                  </Card.Body>
                </Card>
              </Col>
              <Col md={6} className="mb-3">
                <Card className="border-0 bg-light">
                  <Card.Body className="text-center">
                    <FaTag className="text-danger mb-2" size={24} />
                    <h6 className="mb-1">Top Category</h6>
                    <h4 className="text-danger mb-0">
                      {selectedLabel.top_categories && selectedLabel.top_categories.length > 0 
                        ? selectedLabel.top_categories[0].category 
                        : 'N/A'}
                    </h4>
                    {selectedLabel.top_categories && selectedLabel.top_categories.length > 0 && (
                      <small className="text-muted">
                        {formatCurrency(selectedLabel.top_categories[0].amount, preferredCurrency)} spent
                      </small>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            </Row>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDetailModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Labels;
