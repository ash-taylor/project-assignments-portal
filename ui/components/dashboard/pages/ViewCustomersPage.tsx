'use client';

import DashboardViewCard from '@/components/cards/DashboardViewCard';
import ViewCustomers from '@/components/customers/ViewCustomers';

const ViewCustomersPage = () => {
  return (
    <DashboardViewCard title="View Customers">
      <ViewCustomers />
    </DashboardViewCard>
  );
};

export default ViewCustomersPage;
