'use client';

import ProtectedRoute from '@/components/ProtectedRoute';
import Header from '@/components/header/Header';
import Sidebar from '@/components/sidebar/Sidebar';

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <ProtectedRoute>
      <main className="min-h-screen max-h-screen min-w-full max-w-full">
        <div className="flex items-start justify-between">
          <div className="min-w-[300px] border-r min-h-screen">
            <Sidebar />
          </div>

          <div className="grid w-full h-full">
            <Header />
            <div className="p-8">{children}</div>
          </div>
        </div>
      </main>
    </ProtectedRoute>
  );
};
export default DashboardLayout;
