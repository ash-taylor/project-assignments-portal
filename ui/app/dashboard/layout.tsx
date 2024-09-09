'use client';

import ProtectedRoute from '@/components/ProtectedRoute';
import Dashboard from '@/components/dashboard/Dashboard';

const DashboardLayout = () => {
  return (
    <ProtectedRoute>
      <main className="flex min-h-screen w-screen overflow-hidden">
        <Dashboard />
      </main>
    </ProtectedRoute>
  );
};
export default DashboardLayout;
