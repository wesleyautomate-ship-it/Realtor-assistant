import React from 'react';
import { useAppContext } from '../context/AppContext';
import Dashboard from '../pages/Dashboard';
import AdminDashboard from '../pages/AdminDashboard';

const RoleBasedDashboard = () => {
  const { currentUser } = useAppContext();
  
  // Show admin dashboard for admin users, regular dashboard for others
  if (currentUser?.role === 'admin') {
    return <AdminDashboard />;
  }
  
  return <Dashboard />;
};

export default RoleBasedDashboard;
