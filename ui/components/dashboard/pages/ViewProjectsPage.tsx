'use client';

import DashboardViewCard from '@/components/cards/DashboardViewCard';
import ViewProjects from '@/components/projects/ViewProjects';

const ViewProjectsPage = () => {
  return (
    <DashboardViewCard title="View Team Projects">
      <ViewProjects />
    </DashboardViewCard>
  );
};

export default ViewProjectsPage;
