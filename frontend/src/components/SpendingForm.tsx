import React, { useState } from 'react';
import { Card, Form, Button, Row, Col } from 'react-bootstrap';
import { FaPlus } from 'react-icons/fa';
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
    date: getTodayString()
  });

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
        date: getTodayString()
      });
    }
  };

  return (
    <Card className="border-0 shadow-lg" style={{ background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)' }}>
      <Card.Header className="border-0 text-white py-3 py-lg-4">
        <h4 className="mb-0 fw-bold">
          <FaPlus className="me-2 me-lg-3" />
          Add New Spending
        </h4>
        <p className="mb-0 mt-1 mt-lg-2 opacity-75 small">Track your expenses and stay within budget</p>
      </Card.Header>
      <Card.Body className="p-3 p-lg-5 bg-white rounded-bottom">
        <Form onSubmit={handleSubmit}>
          <Row>
            <Col lg={4} xs={12}>
              <Form.Group className="mb-3 mb-lg-4">
                <Form.Label className="fw-bold text-dark mb-2">Amount</Form.Label>
                <Form.Control
                  type="number"
                  step="0.01"
                  min="0"
                  value={form.amount || ''}
                  onChange={(e) => setForm({...form, amount: parseFloat(e.target.value) || 0})}
                  required
                  size="lg"
                  className="border-2"
                  style={{ borderColor: '#e9ecef' }}
                />
              </Form.Group>
            </Col>
            <Col lg={4} xs={12}>
              <CurrencySelector
                value={form.original_currency || 'USD'}
                onChange={(currency) => setForm({...form, original_currency: currency})}
                label="Input Currency"
                size="lg"
              />
            </Col>
            <Col lg={4} xs={12}>
              <Form.Group className="mb-3 mb-lg-4">
                <Form.Label className="fw-bold text-dark mb-2">Date</Form.Label>
                <Form.Control
                  type="date"
                  value={form.date}
                  onChange={(e) => setForm({...form, date: e.target.value})}
                  required
                  size="lg"
                  className="border-2"
                  style={{ borderColor: '#e9ecef' }}
                />
              </Form.Group>
            </Col>
          </Row>

          <Row>
            <Col lg={6} xs={12}>
              <Form.Group className="mb-3 mb-lg-4">
                <Form.Label className="fw-bold text-dark mb-2">Category</Form.Label>
                <Form.Select
                  value={form.category}
                  onChange={(e) => setForm({...form, category: e.target.value})}
                  size="lg"
                  className="border-2"
                  style={{ borderColor: '#e9ecef' }}
                >
                  {CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Col>
            <Col lg={6} xs={12}>
              <Form.Group className="mb-3 mb-lg-4">
                <Form.Label className="fw-bold text-dark mb-2">Location/Store</Form.Label>
                <Form.Control
                  type="text"
                  value={form.location}
                  onChange={(e) => setForm({...form, location: e.target.value})}
                  placeholder="e.g. Walmart, McDonald's"
                  required
                  size="lg"
                  className="border-2"
                  style={{ borderColor: '#e9ecef' }}
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group className="mb-3 mb-lg-4">
            <Form.Label className="fw-bold text-dark mb-2">Description (Optional)</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={form.description}
              onChange={(e) => setForm({...form, description: e.target.value})}
              placeholder="Add notes about this spending..."
              className="border-2"
              style={{ borderColor: '#e9ecef' }}
            />
          </Form.Group>

          <div className="d-grid d-lg-flex d-lg-justify-content-end">
            <Button 
              type="submit" 
              size="lg"
              className="px-4 px-lg-5 py-3 fw-bold"
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
