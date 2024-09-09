'use client';

import DashboardFormCard from '@/components/cards/DashboardFormCard';
import ProjectForm from '@/components/projects/project-form';

const AddProjectPage = () => {
  return (
    <DashboardFormCard title="Add a New Project">
      <ProjectForm formType="add" />
    </DashboardFormCard>
  );
};

export default AddProjectPage;
