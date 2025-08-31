import React from 'react';
import { Card, Row, Col, ProgressBar, Badge } from 'react-bootstrap';
import { FaCalendarDay, FaCalendarAlt, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import { BudgetInfo } from '../types';

interface BudgetOverviewProps {
  budgetInfo: BudgetInfo;
}

export const BudgetOverview: React.FC<BudgetOverviewProps> = ({ budgetInfo }) => {
  const isDailyBudget = budgetInfo.type === 'daily';
  const isOverBudget = isDailyBudget ? budgetInfo.is_over_budget_today : budgetInfo.is_over_budget;
  const percentageUsed = isDailyBudget ? budgetInfo.percentage_used_today : budgetInfo.percentage_used;

  const getBudgetStatus = () => {
    if (isDailyBudget) {
      const remaining = budgetInfo.budget_remaining_today || 0;
      return {
        spent: budgetInfo.today_spending || 0,
        budget: budgetInfo.daily_budget || 0,
        remaining: Math.abs(remaining),
        isOver: remaining < 0,
        message: remaining >= 0 ? `$${remaining.toFixed(2)} left today` : `$${Math.abs(remaining).toFixed(2)} over budget`
      };
    } else {
      const remaining = budgetInfo.budget_remaining || 0;
      return {
        spent: budgetInfo.spent_so_far || 0,
        budget: budgetInfo.total_budget || 0,
        remaining: Math.abs(remaining),
        isOver: remaining < 0,
        message: remaining >= 0 ? `$${remaining.toFixed(2)} left this month` : `$${Math.abs(remaining).toFixed(2)} over budget`
      };
    }
  };

  const status = getBudgetStatus();

  return (
    <Card className="border-0 shadow-sm mb-4" style={{ 
      background: isOverBudget 
        ? 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)' 
        : 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)'
    }}>
      <Card.Body className="p-4">
        <Row className="align-items-center">
          <Col md={2} className="text-center mb-3 mb-md-0">
            <div className={`rounded-circle mx-auto d-flex align-items-center justify-content-center ${
              isOverBudget ? 'bg-danger' : 'bg-success'
            }`} style={{ width: '60px', height: '60px' }}>
              {isDailyBudget ? (
                <FaCalendarDay className="text-white" size={24} />
              ) : (
                <FaCalendarAlt className="text-white" size={24} />
              )}
            </div>
            <h6 className="mt-2 mb-0 fw-bold text-capitalize text-secondary">{budgetInfo.type}</h6>
          </Col>
          
          <Col md={8}>
            <div className="d-flex justify-content-between align-items-center mb-2">
              <h5 className="mb-0 fw-bold text-secondary">Budget Progress</h5>
              <Badge bg={isOverBudget ? 'danger' : 'success'} className="fs-6">
                {isOverBudget ? (
                  <><FaExclamationTriangle className="me-1" />Over Budget</>
                ) : (
                  <><FaCheckCircle className="me-1" />On Track</>
                )}
              </Badge>
            </div>
            
            <div className="d-flex justify-content-between mb-2">
              <span className="text-muted">Spent: <strong className={isOverBudget ? 'text-danger' : 'text-secondary'}>${status.spent.toFixed(2)}</strong></span>
              <span className="text-muted">Budget: <strong>${status.budget.toFixed(2)}</strong></span>
            </div>
            
            <ProgressBar 
              now={Math.min(percentageUsed || 0, 100)} 
              variant={isOverBudget ? 'danger' : 'success'}
              style={{ height: '10px' }}
              className="mb-2"
            />
            
            <div className="d-flex justify-content-between">
              <span className="text-muted small">{(percentageUsed || 0).toFixed(1)}% used</span>
              <span className={`small fw-bold ${status.isOver ? 'text-danger' : 'text-success'}`}>
                {status.message}
              </span>
            </div>
            
            {!isDailyBudget && (
              <div className="mt-2 pt-2 border-top">
                <div className="d-flex justify-content-between small text-muted">
                  <span>Recommended daily: <strong className="text-info">${budgetInfo.recommended_daily?.toFixed(2)}</strong></span>
                  <span>Adjusted daily: <strong className="text-warning">${budgetInfo.adjusted_daily?.toFixed(2)}</strong></span>
                </div>
              </div>
            )}
          </Col>
          
          <Col md={2} className="text-center">
            <h3 className={`mb-0 fw-bold ${status.isOver ? 'text-danger' : 'text-success'}`}>
              ${status.remaining.toFixed(2)}
            </h3>
            <p className="mb-0 text-muted small">{status.isOver ? 'Over' : 'Remaining'}</p>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};
