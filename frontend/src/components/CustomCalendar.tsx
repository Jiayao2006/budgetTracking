import React, { useEffect } from 'react';
import { Table, Badge, Button } from 'react-bootstrap';
import { validateCalendarMonth, dayOfWeekToName, testKnownDates } from '../utils/calendarValidation';

interface CustomCalendarProps {
  selectedDate: string;
  onDateSelect: (date: string) => void;
  spendingsByDate: Record<string, number>;
}

export const CustomCalendar: React.FC<CustomCalendarProps> = ({
  selectedDate,
  onDateSelect,
  spendingsByDate
}) => {
  const parseDate = (dateString: string) => {
    const [year, month, day] = dateString.split('-').map(Number);
    return new Date(year, month - 1, day);
  };

  const formatDate = (date: Date): string => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const currentDate = parseDate(selectedDate);
  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth();

  // Get first day of the month
  const firstDay = new Date(currentYear, currentMonth, 1);
  const lastDay = new Date(currentYear, currentMonth + 1, 0);
  
  // Get starting day of week (0 = Sunday)
  const startingDayOfWeek = firstDay.getDay();
  const daysInMonth = lastDay.getDate();

  // Validate calendar for debugging
  const validation = validateCalendarMonth(currentYear, currentMonth);
  console.log(`Calendar Debug - ${currentYear}/${currentMonth + 1}:`, {
    firstDayOfWeek: startingDayOfWeek,
    firstDayName: dayOfWeekToName(startingDayOfWeek),
    daysInMonth,
    validation
  });

  // Create calendar days array
  const calendarDays: (Date | null)[] = [];
  
  // Add empty cells for days before the first day of the month
  for (let i = 0; i < startingDayOfWeek; i++) {
    calendarDays.push(null);
  }
  
  // Add all days of the month
  for (let day = 1; day <= daysInMonth; day++) {
    calendarDays.push(new Date(currentYear, currentMonth, day));
  }

  // Split into weeks
  const weeks: (Date | null)[][] = [];
  for (let i = 0; i < calendarDays.length; i += 7) {
    weeks.push(calendarDays.slice(i, i + 7));
  }

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const goToPrevMonth = () => {
    const prevMonth = new Date(currentYear, currentMonth - 1, 1);
    onDateSelect(formatDate(prevMonth));
  };

  const goToNextMonth = () => {
    const nextMonth = new Date(currentYear, currentMonth + 1, 1);
    onDateSelect(formatDate(nextMonth));
  };

  const today = new Date();
  const todayString = formatDate(today);

  // Run validation tests on component mount
  useEffect(() => {
    const tests = testKnownDates();
    console.log('Calendar Validation Tests:', tests);
    
    const failedTests = tests.filter(test => !test.correct);
    if (failedTests.length > 0) {
      console.error('Calendar validation failed for:', failedTests);
    } else {
      console.log('✅ All calendar validation tests passed!');
    }
  }, []);

  const runCalendarTest = () => {
    const tests = testKnownDates();
    console.table(tests);
    alert(`Calendar Tests: ${tests.filter(t => t.correct).length}/${tests.length} passed`);
  };

  return (
    <div className="custom-calendar">
      {/* Calendar Header */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <button
          className="btn btn-outline-primary btn-sm"
          onClick={goToPrevMonth}
        >
          ‹ Prev
        </button>
        <div className="text-center">
          <h5 className="mb-0 fw-bold">
            {monthNames[currentMonth]} {currentYear}
          </h5>
          <Button 
            variant="link" 
            size="sm" 
            onClick={runCalendarTest}
            className="text-decoration-none p-0"
            style={{ fontSize: '0.7rem' }}
          >
            🧪 Test Calendar
          </Button>
        </div>
        <button
          className="btn btn-outline-primary btn-sm"
          onClick={goToNextMonth}
        >
          Next ›
        </button>
      </div>

      {/* Calendar Table */}
      <Table bordered hover className="calendar-table mb-0">
        <thead>
          <tr>
            {weekdays.map((day) => (
              <th key={day} className="text-center bg-light py-2">
                <small className="fw-bold text-muted">{day}</small>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeks.map((week, weekIndex) => (
            <tr key={weekIndex}>
              {week.map((date, dayIndex) => {
                const dateString = date ? formatDate(date) : '';
                const isToday = dateString === todayString;
                const isSelected = dateString === selectedDate;
                const hasSpending = dateString && spendingsByDate[dateString];
                
                return (
                  <td
                    key={dayIndex}
                    className={`calendar-cell p-0 position-relative ${
                      !date ? 'empty-cell' : ''
                    } ${isToday ? 'today-cell' : ''} ${
                      isSelected ? 'selected-cell' : ''
                    }`}
                    style={{ 
                      height: '60px', 
                      verticalAlign: 'top',
                      cursor: date ? 'pointer' : 'default'
                    }}
                    onClick={() => {
                      if (date) {
                        onDateSelect(formatDate(date));
                      }
                    }}
                  >
                    {date && (
                      <div className="d-flex flex-column h-100 p-2">
                        <div className="day-number">
                          <small className={`fw-bold ${isToday ? 'text-white' : ''}`}>
                            {date.getDate()}
                          </small>
                        </div>
                        {hasSpending && (
                          <div className="mt-auto">
                            <Badge 
                              bg="danger" 
                              style={{ fontSize: '0.6rem' }}
                            >
                              ${spendingsByDate[dateString].toFixed(0)}
                            </Badge>
                          </div>
                        )}
                      </div>
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};
