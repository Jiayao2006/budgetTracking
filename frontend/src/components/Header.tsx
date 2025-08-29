import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { FaWallet } from 'react-icons/fa';

export const Header: React.FC = () => {
  return (
    <Navbar 
      className="mb-5 shadow-lg" 
      style={{ 
        background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)', 
        minHeight: '80px' 
      }}
      variant="dark"
    >
      <Container>
        <Navbar.Brand className="fs-2 fw-bold">
          <FaWallet className="me-3" size={32} />
          Budget Tracker
        </Navbar.Brand>
        <Navbar.Text className="text-white fs-5 opacity-75">
          Financial Management
        </Navbar.Text>
      </Container>
    </Navbar>
  );
};
