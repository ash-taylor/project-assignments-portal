'use client';

import DashboardFormCard from '@/components/cards/DashboardFormCard';
import CustomerForm from '../../customers/customer-form';

const description =
  'Note: Please create and assign project after customer creation';

const AddCustomerPage = () => {
  return (
    <DashboardFormCard title="Add Customer" description={description}>
      <CustomerForm formType="add" />
    </DashboardFormCard>
  );
};

export default AddCustomerPage;
