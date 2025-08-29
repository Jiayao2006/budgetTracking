// Date utility functions to handle timezone issues consistently

export const formatDateLocal = (date: Date): string => {
  // Format date to YYYY-MM-DD in local timezone
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

export const parseDateLocal = (dateString: string): Date => {
  // Parse YYYY-MM-DD string as local date (avoiding timezone shifts)
  const [year, month, day] = dateString.split('-').map(Number);
  return new Date(year, month - 1, day);
};

export const getTodayString = (): string => {
  // Get today's date as YYYY-MM-DD string in local timezone
  return formatDateLocal(new Date());
};
