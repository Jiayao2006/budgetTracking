import React from 'react';
import { Navbar, Nav, NavDropdown, Container, Badge } from 'react-bootstrap';
import { FaUser, FaSignOutAlt, FaCrown, FaCalendarAlt, FaChartBar, FaCog } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

interface NavigationProps {
  currentPage: string;
  onPageChange: (page: string) => void;
}

export const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange }) => {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <Navbar 
      expand="lg" 
      className="shadow-sm"
      style={{ 
        background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
      }}
    >
      <Container>
        <Navbar.Brand 
          href="#" 
          className="text-white fw-bold d-flex align-items-center"
          onClick={(e) => {
            e.preventDefault();
            onPageChange('calendar');
          }}
        >
          <FaCalendarAlt className="me-2" />
          Budget Tracker
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link
              href="#"
              className={`text-white ${currentPage === 'calendar' ? 'fw-bold' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                onPageChange('calendar');
              }}
            >
              <FaCalendarAlt className="me-1" />
              Calendar
            </Nav.Link>

            <Nav.Link
              href="#"
              className={`text-white ${currentPage === 'settings' ? 'fw-bold' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                onPageChange('settings');
              }}
            >
              <FaCog className="me-1" />
              Settings
            </Nav.Link>
            
            {user.is_admin && (
              <Nav.Link
                href="#"
                className={`text-white ${currentPage === 'admin' ? 'fw-bold' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  onPageChange('admin');
                }}
              >
                <FaCrown className="me-1" />
                Admin Panel
              </Nav.Link>
            )}
          </Nav>
          
          <Nav>
            <NavDropdown
              title={
                <span className="text-white d-flex align-items-center">
                  <FaUser className="me-2" />
                  {user.full_name}
                  {user.is_admin && (
                    <Badge bg="warning" className="ms-2">
                      <FaCrown size={10} />
                    </Badge>
                  )}
                </span>
              }
              id="user-dropdown"
              align="end"
            >
              <NavDropdown.Item disabled>
                <div className="text-muted small">
                  <strong>Email:</strong> {user.email}
                </div>
                <div className="text-muted small">
                  <strong>Role:</strong> {user.is_admin ? 'Administrator' : 'User'}
                </div>
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item
                onClick={logout}
                className="text-danger d-flex align-items-center"
              >
                <FaSignOutAlt className="me-2" />
                Sign Out
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};
