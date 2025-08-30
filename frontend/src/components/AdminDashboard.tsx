import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Button, Badge, Modal, Form, Alert, Spinner } from 'react-bootstrap';
import { FaUsers, FaUserPlus, FaEdit, FaTrash, FaEye, FaCrown, FaChartLine } from 'react-icons/fa';
import { useAuthenticatedFetch } from '../context/AuthContext';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_admin: boolean;
  is_active: boolean;
  created_at: string;
  total_spendings: number;
}

interface AdminStats {
  total_users: number;
  total_admins: number;
  active_users: number;
  inactive_users: number;
  total_spendings: number;
}

interface UserFormData {
  email: string;
  full_name: string;
  password: string;
  is_admin: boolean;
  is_active: boolean;
}

export const AdminDashboard: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [modalType, setModalType] = useState<'create' | 'edit' | 'view'>('create');
  const [formData, setFormData] = useState<UserFormData>({
    email: '',
    full_name: '',
    password: '',
    is_admin: false,
    is_active: true
  });
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const authenticatedFetch = useAuthenticatedFetch();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [usersResponse, statsResponse] = await Promise.all([
        authenticatedFetch('http://localhost:8000/api/admin/users'),
        authenticatedFetch('http://localhost:8000/api/admin/dashboard')
      ]);

      const usersData = await usersResponse.json();
      const statsData = await statsResponse.json();

      setUsers(usersData);
      setStats(statsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleShowModal = (type: 'create' | 'edit' | 'view', user?: User) => {
    setModalType(type);
    setSelectedUser(user || null);
    
    if (type === 'create') {
      setFormData({
        email: '',
        full_name: '',
        password: '',
        is_admin: false,
        is_active: true
      });
    } else if (user) {
      setFormData({
        email: user.email,
        full_name: user.full_name,
        password: '',
        is_admin: user.is_admin,
        is_active: user.is_active
      });
    }
    
    setShowModal(true);
    setError(null);
    setSuccess(null);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedUser(null);
    setError(null);
    setSuccess(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormLoading(true);
    setError(null);

    try {
      let response;
      
      if (modalType === 'create') {
        response = await authenticatedFetch('http://localhost:8000/api/admin/users', {
          method: 'POST',
          body: JSON.stringify(formData),
        });
      } else if (modalType === 'edit' && selectedUser) {
        const updateData = { ...formData };
        if (!updateData.password) {
          delete updateData.password; // Don't send empty password
        }
        
        response = await authenticatedFetch(`http://localhost:8000/api/admin/users/${selectedUser.id}`, {
          method: 'PUT',
          body: JSON.stringify(updateData),
        });
      }

      if (response && !response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Operation failed');
      }

      setSuccess(modalType === 'create' ? 'User created successfully!' : 'User updated successfully!');
      loadDashboardData();
      
      setTimeout(() => {
        handleCloseModal();
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Operation failed');
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async (userId: number) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      const response = await authenticatedFetch(`http://localhost:8000/api/admin/users/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Delete failed');
      }

      setSuccess('User deleted successfully!');
      loadDashboardData();
      
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed');
      setTimeout(() => setError(null), 3000);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '400px' }}>
        <Spinner animation="border" variant="primary" />
      </Container>
    );
  }

  return (
    <Container fluid className="p-4">
      <Row className="mb-4">
        <Col>
          <h2 className="mb-0">
            <FaCrown className="me-2 text-warning" />
            Admin Dashboard
          </h2>
          <p className="text-muted">Manage users and view system statistics</p>
        </Col>
      </Row>

      {error && (
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert variant="success" dismissible onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Statistics Cards */}
      {stats && (
        <Row className="mb-4">
          <Col md={3} sm={6} className="mb-3">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <FaUsers className="text-primary mb-2" size={24} />
                <h4 className="mb-1">{stats.total_users}</h4>
                <small className="text-muted">Total Users</small>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} sm={6} className="mb-3">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <FaCrown className="text-warning mb-2" size={24} />
                <h4 className="mb-1">{stats.total_admins}</h4>
                <small className="text-muted">Administrators</small>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} sm={6} className="mb-3">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <div className="text-success mb-2">●</div>
                <h4 className="mb-1">{stats.active_users}</h4>
                <small className="text-muted">Active Users</small>
              </Card.Body>
            </Card>
          </Col>
          <Col md={3} sm={6} className="mb-3">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <FaChartLine className="text-info mb-2" size={24} />
                <h4 className="mb-1">{formatCurrency(stats.total_spendings)}</h4>
                <small className="text-muted">Total Spendings</small>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Users Table */}
      <Card className="border-0 shadow-sm">
        <Card.Header className="bg-white border-bottom">
          <Row className="align-items-center">
            <Col>
              <h5 className="mb-0">Users Management</h5>
            </Col>
            <Col xs="auto">
              <Button
                variant="primary"
                onClick={() => handleShowModal('create')}
                className="d-flex align-items-center"
              >
                <FaUserPlus className="me-2" />
                Add User
              </Button>
            </Col>
          </Row>
        </Card.Header>
        <Card.Body className="p-0">
          <div className="table-responsive">
            <Table hover className="mb-0">
              <thead className="bg-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Join Date</th>
                  <th>Total Spending</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.full_name}</td>
                    <td>{user.email}</td>
                    <td>
                      {user.is_admin ? (
                        <Badge bg="warning" className="d-flex align-items-center w-fit">
                          <FaCrown className="me-1" />
                          Admin
                        </Badge>
                      ) : (
                        <Badge bg="secondary">User</Badge>
                      )}
                    </td>
                    <td>
                      <Badge bg={user.is_active ? 'success' : 'danger'}>
                        {user.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </td>
                    <td>{formatDate(user.created_at)}</td>
                    <td>{formatCurrency(user.total_spendings)}</td>
                    <td>
                      <div className="d-flex gap-2">
                        <Button
                          variant="outline-info"
                          size="sm"
                          onClick={() => handleShowModal('view', user)}
                        >
                          <FaEye />
                        </Button>
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => handleShowModal('edit', user)}
                        >
                          <FaEdit />
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(user.id)}
                        >
                          <FaTrash />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>

      {/* User Modal */}
      <Modal show={showModal} onHide={handleCloseModal} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            {modalType === 'create' && 'Create New User'}
            {modalType === 'edit' && 'Edit User'}
            {modalType === 'view' && 'User Details'}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && <Alert variant="success">{success}</Alert>}
          
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Full Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                    required
                    disabled={modalType === 'view'}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                    disabled={modalType === 'view'}
                  />
                </Form.Group>
              </Col>
            </Row>

            {modalType !== 'view' && (
              <Form.Group className="mb-3">
                <Form.Label>
                  Password {modalType === 'edit' && '(leave blank to keep current)'}
                </Form.Label>
                <Form.Control
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  required={modalType === 'create'}
                  minLength={6}
                />
              </Form.Group>
            )}

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Administrator"
                    checked={formData.is_admin}
                    onChange={(e) => setFormData({...formData, is_admin: e.target.checked})}
                    disabled={modalType === 'view'}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Check
                    type="checkbox"
                    label="Active"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
                    disabled={modalType === 'view'}
                  />
                </Form.Group>
              </Col>
            </Row>

            {modalType !== 'view' && (
              <div className="d-flex justify-content-end gap-2">
                <Button variant="secondary" onClick={handleCloseModal}>
                  Cancel
                </Button>
                <Button type="submit" variant="primary" disabled={formLoading}>
                  {formLoading ? (
                    <>
                      <Spinner animation="border" size="sm" className="me-2" />
                      {modalType === 'create' ? 'Creating...' : 'Updating...'}
                    </>
                  ) : (
                    modalType === 'create' ? 'Create User' : 'Update User'
                  )}
                </Button>
              </div>
            )}
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
  );
};
