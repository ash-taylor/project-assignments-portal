'use client';

import DashboardViewCard from '@/components/cards/DashboardViewCard';
import ViewUsers from '@/components/users/ViewUsers';
const ViewUsersPage = () => {
  return (
    <DashboardViewCard title="Manage Team">
      <ViewUsers />
    </DashboardViewCard>
  );
};

export default ViewUsersPage;
