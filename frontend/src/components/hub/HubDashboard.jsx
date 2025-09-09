import React from 'react';
import { useAppContext } from '../../context/AppContext';
import AgentDashboard from './AgentDashboard';
import OwnerDashboard from './OwnerDashboard';

const HubDashboard = () => {
  const { currentUser } = useAppContext();

  // Determine which dashboard to show based on user role
  const isOwner = currentUser?.role === 'brokerage_owner' || currentUser?.role === 'admin';
  const isAgent = currentUser?.role === 'agent';

  // Default to agent dashboard if role is not clearly defined
  if (isOwner) {
    return <OwnerDashboard />;
  }

  return <AgentDashboard />;
};

export default HubDashboard;
