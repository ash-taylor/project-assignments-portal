'use client';

import { useState } from 'react';

import DashboardHome from './DashboardHome';
import AddCustomerPage from './AddCustomerPage';

import Header from './header/Header';
import Sidebar from './sidebar/Sidebar';

const Dashboard = () => {
  const [currentPage, setCurrentPage] = useState<string>('/dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case '/dashboard':
        return <DashboardHome />;
      case '/add-customer':
        return <AddCustomerPage />;
      default:
        return <DashboardHome />;
    }
  };

  return (
    <>
      <div className="min-w-[300px] border-r min-h-screen">
        <Sidebar onNavigate={setCurrentPage} />
      </div>
      <div className="grid w-full h-full">
        <Header />
        <div className="p-8">{renderPage()}</div>
      </div>
    </>
  );
};

export default Dashboard;
