import React, { useState, useEffect } from 'react';
import { Row, Col, Card, ListGroup, Button, Modal, Form, Badge } from 'react-bootstrap';
import { FaEdit, FaTrash, FaSave, FaTimes, FaCalendarAlt, FaShoppingCart, FaCalendarDay } from 'react-icons/fa';
import { Spending, SpendingCreate } from '../types';
import { formatDateLocal, parseDateLocal } from '../utils/dateUtils';
import { CustomCalendar } from './CustomCalendar';
import '../styles/custom-calendar.css';

interface SpendingCalendarProps {
  spendings: Spending[];
  onDateSelect: (date: string) => void;
  selectedDate: string;
  onUpdateSpending: (id: number, spending: SpendingCreate) => void;
  onDeleteSpending: (id: number) => void;
}

const CATEGORIES = [
  'Food', 'Fashion', 'Transportation', 'Entertainment', 
  'Health', 'Education', 'Utilities', 'Shopping', 'Other'
];

export const SpendingCalendar: React.FC<SpendingCalendarProps> = ({ 
  spendings, 
  onDateSelect, 
  selectedDate,
  onUpdateSpending,
  onDeleteSpending
}) => {
  const [selectedDateSpendings, setSelectedDateSpendings] = useState<Spending[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<SpendingCreate>({
    amount: 0,
    category: 'Food',
    location: '',
    description: '',
    date: ''
  });
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // Get spending totals by date
  const spendingsByDate = (spendings || []).reduce((acc, spending) => {
    const date = spending.date;
    acc[date] = (acc[date] || 0) + spending.amount;
    return acc;
  }, {} as Record<string, number>);

  useEffect(() => {
    const dateSpends = (spendings || []).filter(s => s.date === selectedDate);
    setSelectedDateSpendings(dateSpends);
  }, [spendings, selectedDate]);

  const startEdit = (spending: Spending) => {
    setEditingId(spending.id);
    setEditForm({
      amount: spending.amount,
      category: spending.category,
      location: spending.location,
      description: spending.description || '',
      date: spending.date
    });
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditForm({ amount: 0, category: 'Food', location: '', description: '', date: '' });
  };

  const saveEdit = () => {
    if (editingId && editForm.amount > 0 && editForm.location.trim()) {
      onUpdateSpending(editingId, editForm);
      cancelEdit();
    }
  };

  const confirmDelete = (id: number) => {
    setDeletingId(id);
    setShowDeleteModal(true);
  };

  const handleDelete = () => {
    if (deletingId) {
      onDeleteSpending(deletingId);
      setShowDeleteModal(false);
      setDeletingId(null);
    }
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      'Food': 'success',
      'Fashion': 'danger',
      'Transportation': 'warning',
      'Entertainment': 'info',
      'Health': 'secondary',
      'Education': 'primary',
      'Utilities': 'dark',
      'Shopping': 'light',
      'Other': 'secondary'
    };
    return colors[category] || 'secondary';
  };

  return (
    <div className="spending-calendar-container">
      <Row>
        <Col lg={6} className="mb-4">
          <Card className="border-0 shadow-lg" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
            <Card.Header className="border-0 text-white py-3 py-lg-4">
              <div className="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center">
                <div className="mb-2 mb-sm-0">
                  <h4 className="mb-0 fw-bold">
                    <FaCalendarAlt className="me-2 me-lg-3" />
                    Spending Calendar
                  </h4>
                  <p className="mb-0 mt-1 mt-lg-2 opacity-75 small">Click on a date to view your daily expenses</p>
                </div>
                <Button
                  className="today-btn"
                  size="sm"
                  onClick={() => onDateSelect(formatDateLocal(new Date()))}
                >
                  <FaCalendarDay className="me-1 me-sm-2" />
                  <span className="d-none d-sm-inline">Today</span>
                  <span className="d-sm-none">Today</span>
                </Button>
              </div>
            </Card.Header>
            <Card.Body className="p-3 p-lg-5 bg-white rounded-bottom">
              <CustomCalendar
                selectedDate={selectedDate}
                onDateSelect={onDateSelect}
                spendingsByDate={spendingsByDate}
              />
            </Card.Body>
          </Card>
        </Col>

        <Col lg={6}>
          <Card className="border-0 shadow-lg" style={{ background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)' }}>
            <Card.Header className="border-0 text-white py-3 py-lg-4">
              <div className="d-flex flex-column flex-sm-row justify-content-between align-items-start align-items-sm-center">
                <div className="mb-2 mb-sm-0">
                  <h4 className="mb-0 fw-bold">
                    <FaShoppingCart className="me-2 me-lg-3" />
                    Daily Expenses
                  </h4>
                  <p className="mb-0 mt-1 mt-lg-2 opacity-75 small">{parseDateLocal(selectedDate).toLocaleDateString()}</p>
                </div>
                <Badge bg="light" text="dark" className="fs-6 px-2 px-sm-3 py-2">
                  Total: ${selectedDateSpendings.reduce((sum, s) => sum + s.amount, 0).toFixed(2)}
                </Badge>
              </div>
            </Card.Header>
            <Card.Body className="p-3 p-lg-5 bg-white rounded-bottom" style={{ maxHeight: '500px', overflowY: 'auto' }}>
              {selectedDateSpendings.length === 0 ? (
                <div className="text-center text-muted py-4 py-lg-5">
                  <FaShoppingCart size={32} className="mb-3 opacity-50 d-lg-none" />
                  <FaShoppingCart size={48} className="mb-3 opacity-50 d-none d-lg-block" />
                  <p className="h6 h5-lg mb-2">No expenses for this date</p>
                  <p className="mb-0 text-secondary small">Start tracking your spending!</p>
                </div>
              ) : (
                <ListGroup variant="flush">
                  {selectedDateSpendings.map((spending) => (
                    <ListGroup.Item key={spending.id}>
                      {editingId === spending.id ? (
                        <Form>
                          <Row className="mb-2">
                            <Col xs={12} sm={6}>
                              <Form.Control
                                type="number"
                                step="0.01"
                                min="0"
                                value={editForm.amount || ''}
                                onChange={(e) => setEditForm({...editForm, amount: parseFloat(e.target.value) || 0})}
                                placeholder="Amount"
                                size="sm"
                              />
                            </Col>
                            <Col xs={12} sm={6} className="mt-2 mt-sm-0">
                              <Form.Select
                                value={editForm.category}
                                onChange={(e) => setEditForm({...editForm, category: e.target.value})}
                                size="sm"
                              >
                                {CATEGORIES.map(cat => (
                                  <option key={cat} value={cat}>{cat}</option>
                                ))}
                              </Form.Select>
                            </Col>
                          </Row>
                          <Row className="mb-2">
                            <Col xs={12}>
                              <Form.Control
                                type="text"
                                value={editForm.location}
                                onChange={(e) => setEditForm({...editForm, location: e.target.value})}
                                placeholder="Location"
                                size="sm"
                              />
                            </Col>
                          </Row>
                          <Row className="mb-2">
                            <Col xs={12}>
                              <Form.Control
                                as="textarea"
                                rows={2}
                                value={editForm.description}
                                onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                                placeholder="Description"
                                size="sm"
                              />
                            </Col>
                          </Row>
                          <div className="d-flex flex-column flex-sm-row gap-2">
                            <Button variant="success" size="sm" onClick={saveEdit} className="flex-fill">
                              <FaSave className="me-1" />
                              Save
                            </Button>
                            <Button variant="secondary" size="sm" onClick={cancelEdit} className="flex-fill">
                              <FaTimes className="me-1" />
                              Cancel
                            </Button>
                          </div>
                        </Form>
                      ) : (
                        <div>
                          <div className="d-flex flex-column flex-sm-row justify-content-between align-items-start mb-2">
                            <div className="flex-grow-1 w-100 w-sm-auto mb-2 mb-sm-0">
                              <h6 className="mb-1 fw-bold">{spending.location}</h6>
                              <div className="mb-1 d-flex flex-wrap align-items-center gap-2">
                                <Badge bg={getCategoryColor(spending.category)} className="me-0">
                                  {spending.category}
                                </Badge>
                                <span className="text-muted small">
                                  {parseDateLocal(spending.date).toLocaleDateString()}
                                </span>
                              </div>
                              {spending.description && (
                                <p className="text-muted small mb-0">{spending.description}</p>
                              )}
                            </div>
                            <div className="d-flex flex-row flex-sm-column align-items-center align-items-sm-end justify-content-between w-100 w-sm-auto">
                              <div className="h5 text-danger mb-0 mb-sm-2">${spending.amount.toFixed(2)}</div>
                              <div className="d-flex gap-1">
                                <Button 
                                  variant="outline-primary" 
                                  size="sm" 
                                  onClick={() => startEdit(spending)}
                                >
                                  <FaEdit />
                                </Button>
                                <Button 
                                  variant="outline-danger" 
                                  size="sm" 
                                  onClick={() => confirmDelete(spending.id)}
                                >
                                  <FaTrash />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Delete Confirmation Modal */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete this spending? This action cannot be undone.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            <FaTrash className="me-1" />
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};
