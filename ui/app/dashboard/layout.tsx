'use client';

import ProtectedRoute from '@/components/ProtectedRoute';
import Dashboard from '@/components/dashboard/Dashboard';

const DashboardLayout = () => {
  return (
    <ProtectedRoute>
      <main className="min-h-screen max-h-screen min-w-full max-w-full">
        <div className="flex items-start justify-between">
          <Dashboard />
        </div>
      </main>
    </ProtectedRoute>
  );
};
export default DashboardLayout;
