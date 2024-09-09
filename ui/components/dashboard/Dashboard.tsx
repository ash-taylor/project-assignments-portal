'use client';

import { useState } from 'react';

import AddCustomerPage from './pages/AddCustomerPage';
import Header from './header/Header';
import Sidebar from './sidebar/Sidebar';
import DashboardHome from './pages/DashboardHome';
import ViewCustomersPage from './pages/ViewCustomersPage';
import ViewProjectsPage from './pages/ViewProjectsPage';
import AddProjectPage from './pages/AddProjectPage';

const Dashboard = () => {
  const [currentPage, setCurrentPage] = useState<string>('/dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case '/dashboard':
        return <DashboardHome />;
      case '/add-customer':
        return <AddCustomerPage />;
      case '/view-customers':
        return <ViewCustomersPage />;
      case '/add-project':
        return <AddProjectPage />;
      case '/view-projects':
        return <ViewProjectsPage />;
      default:
        return <DashboardHome />;
    }
  };

  return (
    <>
      <div className="fixed w-[300px] h-screen overflow-y-auto border-r bg-white z-50">
        <Sidebar onNavigate={setCurrentPage} />
      </div>
      <div className="fixed ml-[300px] flex flex-col w-[calc(100%-300px)]">
        <Header />
        <div className="h-[calc(100vh-100px)] p-8 overflow-y-auto">
          {renderPage()}
        </div>
      </div>
    </>
  );
};

export default Dashboard;
