import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { FaUser, FaLock, FaEnvelope, FaUserPlus, FaSignInAlt } from 'react-icons/fa';

interface AuthPageProps {
  onLogin: (email: string, password: string) => Promise<void>;
  onRegister: (email: string, password: string, fullName: string) => Promise<void>;
  loading: boolean;
  error: string | null;
}

export const AuthPage: React.FC<AuthPageProps> = ({ onLogin, onRegister, loading, error }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    fullName: '',
    confirmPassword: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isLogin) {
      if (formData.password !== formData.confirmPassword) {
        return;
      }
      if (formData.password.length < 6) {
        return;
      }
      await onRegister(formData.email, formData.password, formData.fullName);
    } else {
      await onLogin(formData.email, formData.password);
    }
  };

  const resetForm = () => {
    setFormData({
      email: '',
      password: '',
      fullName: '',
      confirmPassword: ''
    });
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    resetForm();
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center'
    }}>
      <Container>
        <Row className="justify-content-center">
          <Col md={6} lg={5} xl={4}>
            <Card className="shadow-lg border-0" style={{ borderRadius: '15px' }}>
              <Card.Header 
                className="text-center py-4 border-0"
                style={{ 
                  background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                  borderRadius: '15px 15px 0 0'
                }}
              >
                <h3 className="text-white mb-0 fw-bold">
                  {isLogin ? (
                    <>
                      <FaSignInAlt className="me-2" />
                      Welcome Back
                    </>
                  ) : (
                    <>
                      <FaUserPlus className="me-2" />
                      Create Account
                    </>
                  )}
                </h3>
                <p className="text-white-50 mb-0 mt-2">
                  {isLogin ? 'Sign in to your budget tracker' : 'Join us to start tracking your expenses'}
                </p>
              </Card.Header>
              
              <Card.Body className="p-4">
                {error && (
                  <Alert variant="danger" className="mb-3">
                    {error}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  {!isLogin && (
                    <Form.Group className="mb-3">
                      <Form.Label className="fw-bold">
                        <FaUser className="me-2" />
                        Full Name
                      </Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Enter your full name"
                        value={formData.fullName}
                        onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                        required={!isLogin}
                        size="lg"
                        className="border-2"
                      />
                    </Form.Group>
                  )}

                  <Form.Group className="mb-3">
                    <Form.Label className="fw-bold">
                      <FaEnvelope className="me-2" />
                      Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      required
                      size="lg"
                      className="border-2"
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label className="fw-bold">
                      <FaLock className="me-2" />
                      Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={(e) => setFormData({...formData, password: e.target.value})}
                      required
                      size="lg"
                      className="border-2"
                      minLength={isLogin ? 1 : 6}
                    />
                    {!isLogin && (
                      <Form.Text className="text-muted">
                        Password must be at least 6 characters long.
                      </Form.Text>
                    )}
                  </Form.Group>

                  {!isLogin && (
                    <Form.Group className="mb-3">
                      <Form.Label className="fw-bold">
                        <FaLock className="me-2" />
                        Confirm Password
                      </Form.Label>
                      <Form.Control
                        type="password"
                        placeholder="Confirm your password"
                        value={formData.confirmPassword}
                        onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                        required={!isLogin}
                        size="lg"
                        className="border-2"
                      />
                      {formData.password !== formData.confirmPassword && formData.confirmPassword && (
                        <Form.Text className="text-danger">
                          Passwords do not match.
                        </Form.Text>
                      )}
                    </Form.Group>
                  )}

                  <div className="d-grid mb-3">
                    <Button
                      type="submit"
                      size="lg"
                      disabled={loading}
                      style={{
                        background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                        border: 'none',
                        borderRadius: '10px'
                      }}
                    >
                      {loading ? (
                        <>
                          <Spinner animation="border" size="sm" className="me-2" />
                          {isLogin ? 'Signing In...' : 'Creating Account...'}
                        </>
                      ) : (
                        <>
                          {isLogin ? (
                            <>
                              <FaSignInAlt className="me-2" />
                              Sign In
                            </>
                          ) : (
                            <>
                              <FaUserPlus className="me-2" />
                              Create Account
                            </>
                          )}
                        </>
                      )}
                    </Button>
                  </div>
                </Form>

                <div className="text-center">
                  <span className="text-muted">
                    {isLogin ? "Don't have an account? " : "Already have an account? "}
                  </span>
                  <Button
                    variant="link"
                    onClick={toggleMode}
                    className="p-0 text-decoration-none fw-bold"
                    style={{ color: '#4f46e5' }}
                  >
                    {isLogin ? 'Sign Up' : 'Sign In'}
                  </Button>
                </div>

                {isLogin && (
                  <div className="text-center mt-3">
                    <small className="text-muted">
                      <strong>Demo Admin:</strong> admin@budgettracker.com / admin123
                    </small>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};
