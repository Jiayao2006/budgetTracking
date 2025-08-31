import React, { useState, useEffect } from 'react';
import { Card, Form, Button, Row, Col, InputGroup } from 'react-bootstrap';
import { FaPlus, FaMoneyBillWave, FaCalendarAlt, FaShoppingBag, FaMapMarkerAlt, FaTag, FaFileAlt } from 'react-icons/fa';
import { SpendingCreate } from '../types';
import { getTodayString } from '../utils/dateUtils';
import { CurrencySelector } from './CurrencySelector';

interface SpendingFormProps {
  onSubmit: (spending: SpendingCreate) => void;
}

const CATEGORIES = [
  'Food', 'Fashion', 'Transportation', 'Entertainment', 
  'Health', 'Education', 'Utilities', 'Shopping', 'Other'
];

export const SpendingForm: React.FC<SpendingFormProps> = ({ onSubmit }) => {
  const [form, setForm] = useState<SpendingCreate>({
    amount: 0,
    original_currency: 'USD',
    category: 'Food',
    location: '',
    description: '',
    label: '',
    date: getTodayString()
  });
  
  const [existingLabels, setExistingLabels] = useState<string[]>([]);
  const [isCustomLabel, setIsCustomLabel] = useState(false);

  useEffect(() => {
    fetchExistingLabels();
  }, []);

  const fetchExistingLabels = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch('/api/labels/list', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const labels: string[] = await response.json();
        setExistingLabels(labels);
      }
    } catch (error) {
      console.error('Error fetching existing labels:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.amount > 0 && form.location.trim()) {
      onSubmit(form);
      setForm({
        amount: 0,
        original_currency: 'USD',
        category: 'Food',
        location: '',
        description: '',
        label: '',
        date: getTodayString()
      });
      setIsCustomLabel(false);
      fetchExistingLabels(); // Refresh labels list
    }
  };

  return (
    <Card className="border-0 shadow-lg rounded-4 overflow-hidden" style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)' }}>
      <Card.Header className="border-0 text-white py-4">
        <h4 className="mb-0 fw-bold d-flex align-items-center">
          <FaPlus className="me-3" />
          Add New Spending
        </h4>
        <p className="mb-0 mt-2 opacity-75 small">Track your expenses and stay within budget</p>
      </Card.Header>
      <Card.Body className="p-4 p-lg-5 bg-white rounded-bottom">
        <Form onSubmit={handleSubmit}>
          <Row className="g-4">
            <Col lg={4} md={6} xs={12}>
              <Form.Group>
                <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
                  <FaMoneyBillWave className="text-primary me-2" />
                  Amount
                </Form.Label>
                <InputGroup>
                  <Form.Control
                    type="number"
                    step="0.01"
                    min="0"
                    value={form.amount || ''}
                    onChange={(e) => setForm({...form, amount: parseFloat(e.target.value) || 0})}
                    required
                    placeholder="0.00"
                    className="shadow-sm border-2"
                    style={{ borderColor: '#e9ecef', borderRight: 'none' }}
                  />
                  <InputGroup.Text className="bg-white border-2" style={{ borderColor: '#e9ecef', borderLeft: 'none' }}>
                    {form.original_currency}
                  </InputGroup.Text>
                </InputGroup>
              </Form.Group>
            </Col>
            <Col lg={4} md={6} xs={12}>
              <CurrencySelector
                value={form.original_currency || 'USD'}
                onChange={(currency) => setForm({...form, original_currency: currency})}
                label={
                  <span className="d-flex align-items-center">
                    <FaMoneyBillWave className="text-primary me-2" />
                    Input Currency
                  </span>
                }
              />
            </Col>
            <Col lg={4} md={6} xs={12}>
              <Form.Group>
                <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
                  <FaCalendarAlt className="text-primary me-2" />
                  Date
                </Form.Label>
                <Form.Control
                  type="date"
                  value={form.date}
                  onChange={(e) => setForm({...form, date: e.target.value})}
                  required
                  className="shadow-sm border-2"
                  style={{ borderColor: '#e9ecef' }}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row className="g-4 mt-2">
            <Col lg={6} md={6} xs={12}>
              <Form.Group>
                <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
                  <FaShoppingBag className="text-primary me-2" />
                  Category
                </Form.Label>
                <Form.Select
                  value={form.category}
                  onChange={(e) => setForm({...form, category: e.target.value})}
                  className="shadow-sm border-2"
                  style={{ borderColor: '#e9ecef' }}
                >
                  {CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col lg={6} md={6} xs={12}>
              <Form.Group>
                <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
                  <FaMapMarkerAlt className="text-primary me-2" />
                  Location/Store
                </Form.Label>
                <Form.Control
                  type="text"
                  value={form.location}
                  onChange={(e) => setForm({...form, location: e.target.value})}
                  placeholder="e.g. Walmart, McDonald's"
                  required
                  className="shadow-sm border-2"
                  style={{ borderColor: '#e9ecef' }}
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mt-4">
            <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
              <FaTag className="text-primary me-2" />
              Label (Optional)
            </Form.Label>
            <Row className="g-3">
              <Col md={isCustomLabel ? 6 : 12}>
                <Form.Select
                  value={isCustomLabel ? 'custom' : form.label || ''}
                  onChange={(e) => {
                    const value = e.target.value;
                    if (value === 'custom') {
                      setIsCustomLabel(true);
                      setForm({...form, label: ''});
                    } else {
                      setIsCustomLabel(false);
                      setForm({...form, label: value});
                    }
                  }}
                  className="shadow-sm border-2"
                  style={{ borderColor: '#e9ecef' }}
                >
                  <option value="">No label</option>
                  {existingLabels.map((label) => (
                    <option key={label} value={label}>
                      {label}
                    </option>
                  ))}
                  <option value="custom">+ Create new label</option>
                </Form.Select>
              </Col>
              {isCustomLabel && (
                <Col md={6}>
                  <Form.Control
                    type="text"
                    value={form.label}
                    onChange={(e) => setForm({...form, label: e.target.value})}
                    placeholder="Enter new label name"
                    className="shadow-sm border-2"
                    style={{ borderColor: '#e9ecef' }}
                  />
                </Col>
              )}
            </Row>
            <Form.Text className="text-muted mt-2 d-block">
              Select an existing label or create a new one to categorize this spending
            </Form.Text>
          </Form.Group>

          <Form.Group className="mt-4">
            <Form.Label className="fw-bold text-secondary mb-2 d-flex align-items-center">
              <FaFileAlt className="text-primary me-2" />
              Description (Optional)
            </Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={form.description}
              onChange={(e) => setForm({...form, description: e.target.value})}
              placeholder="Add notes about this spending..."
              className="shadow-sm border-2"
              style={{ borderColor: '#e9ecef' }}
            />
          </Form.Group>

          <div className="d-grid d-md-flex justify-content-md-end mt-4">
            <Button 
              type="submit" 
              size="lg"
              className="px-5 py-3 fw-bold shadow-sm"
              style={{ 
                background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)', 
                border: 'none',
                borderRadius: '12px'
              }}
            >
              <FaPlus className="me-2" />
              Add Spending
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};
