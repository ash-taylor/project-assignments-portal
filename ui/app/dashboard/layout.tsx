import type { Metadata } from 'next';
import ProtectedRoute from '@/components/ProtectedRoute';
import Sidebar from '@/components/sidebar/Sidebar';

export const metadata: Metadata = {
  title: 'Project Assignments Portal - Dashboard',
};

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <ProtectedRoute>
      <div className="min-h-screen max-h-screen w-full flex">
        <Sidebar />
        {children}
      </div>
    </ProtectedRoute>
  );
};

export default DashboardLayout;
