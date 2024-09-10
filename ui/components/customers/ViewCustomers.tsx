'use client';

import { AxiosError } from 'axios';
import { useCallback, useContext, useEffect, useState } from 'react';

import Customer from './customer';
import { useToast } from '@/hooks/use-toast';
import { getCustomers } from '@/lib/api';
import { CustomerResponse } from '@/models/Customer';
import { LoadingSpinner } from '../ui/loading-spinner';
import AuthContext from '@/context/AuthContext';

const ViewCustomers = () => {
  const [customers, setCustomers] = useState<CustomerResponse[] | undefined>(
    undefined
  );
  const [isReady, setIsReady] = useState<boolean>(false);

  const { toast } = useToast();
  const { logout } = useContext(AuthContext);

  const fetchCustomers = useCallback(async () => {
    try {
      const response = await getCustomers();

      setCustomers(response.data);

      setIsReady(true);
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          toast({
            title: 'Session Expired',
            description: 'Your credentials have expired, you must log in again',
            variant: 'destructive',
          });
          setTimeout(() => {
            return logout();
          }, 3000);
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Customers',
            description: error.message,
          });
        }
      }
    }
  }, [logout, toast]);

  const handleRefresh = () => {
    setCustomers(undefined);
    setIsReady(false);
    fetchCustomers();
  };

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  useEffect(() => {
    if (customers) setIsReady(true);
  }, [customers]);

  return (
    <>
      {isReady ? (
        customers?.map((customer, idx) => (
          <Customer
            key={idx}
            customer={customer}
            handleRefresh={handleRefresh}
          />
        ))
      ) : (
        <div className="flex items-center justify-center h-full w-full">
          <LoadingSpinner message="Loading customers..." />
        </div>
      )}
    </>
  );
};
export default ViewCustomers;
