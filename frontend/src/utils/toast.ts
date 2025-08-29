export const showSuccessToast = (message: string) => {
  console.log('✅ SUCCESS:', message);
  // You can implement a proper toast library here
};

export const showErrorToast = (message: string) => {
  console.error('❌ ERROR:', message);
  alert(`Error: ${message}`);
};

export const showInfoToast = (message: string) => {
  console.log('ℹ️ INFO:', message);
  // You can implement a proper toast library here
};
