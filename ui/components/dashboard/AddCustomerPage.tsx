'use client';

import AddCustomerCard from '../cards/AddCustomer';
import CustomerForm from '../customers/customer-form';

const AddCustomerPage = () => {
  return (
    <AddCustomerCard>
      <CustomerForm formType="add" />
    </AddCustomerCard>
  );
};

export default AddCustomerPage;
