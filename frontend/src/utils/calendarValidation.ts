/**
 * Calendar Date Validation Utilities
 * This file contains functions to validate calendar layout correctness
 */

interface CalendarValidation {
  year: number;
  month: number; // 0-based (0 = January)
  firstDayOfWeek: number; // 0 = Sunday
  daysInMonth: number;
  isValid: boolean;
  errors: string[];
}

/**
 * Validates the calendar layout for a given year and month
 */
export const validateCalendarMonth = (year: number, month: number): CalendarValidation => {
  const errors: string[] = [];
  
  // Create first day of the month
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  
  const firstDayOfWeek = firstDay.getDay(); // 0 = Sunday
  const daysInMonth = lastDay.getDate();
  
  // Validation checks
  if (month < 0 || month > 11) {
    errors.push('Invalid month: must be between 0-11');
  }
  
  if (year < 1900 || year > 2100) {
    errors.push('Invalid year: must be between 1900-2100');
  }
  
  if (firstDayOfWeek < 0 || firstDayOfWeek > 6) {
    errors.push('Invalid first day of week calculation');
  }
  
  if (daysInMonth < 28 || daysInMonth > 31) {
    errors.push('Invalid days in month calculation');
  }
  
  return {
    year,
    month,
    firstDayOfWeek,
    daysInMonth,
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Gets the correct day of week for the first day of any month
 */
export const getFirstDayOfMonth = (year: number, month: number): number => {
  return new Date(year, month, 1).getDay();
};

/**
 * Test function to verify calendar correctness for known dates
 */
export const testKnownDates = (): { date: string; expected: number; actual: number; correct: boolean }[] => {
  const testCases = [
    { year: 2025, month: 0, expected: 3 }, // January 1, 2025 is a Wednesday (3)
    { year: 2025, month: 1, expected: 6 }, // February 1, 2025 is a Saturday (6)
    { year: 2025, month: 7, expected: 5 }, // August 1, 2025 is a Friday (5)
    { year: 2024, month: 0, expected: 1 }, // January 1, 2024 was a Monday (1)
    { year: 2024, month: 11, expected: 0 }, // December 1, 2024 was a Sunday (0)
  ];
  
  return testCases.map(testCase => {
    const actual = getFirstDayOfMonth(testCase.year, testCase.month);
    return {
      date: `${testCase.year}-${String(testCase.month + 1).padStart(2, '0')}-01`,
      expected: testCase.expected,
      actual,
      correct: actual === testCase.expected
    };
  });
};

/**
 * Format day of week number to name
 */
export const dayOfWeekToName = (day: number): string => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[day] || 'Invalid';
};

export default {
  validateCalendarMonth,
  getFirstDayOfMonth,
  testKnownDates,
  dayOfWeekToName
};
