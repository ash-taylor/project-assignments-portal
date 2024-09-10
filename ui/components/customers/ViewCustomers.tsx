'use client';

import { useCallback, useEffect, useState } from 'react';
import { CustomerResponse } from '@/models/Customer';
import { getCustomers } from '@/lib/api';
import Customer from './customer';
import { LoadingSpinner } from '../ui/loading-spinner';
import { AxiosError } from 'axios';
import { useToast } from '@/hooks/use-toast';

const ViewCustomers = () => {
  const [customers, setCustomers] = useState<CustomerResponse[] | undefined>(
    undefined
  );
  const [isReady, setIsReady] = useState<boolean>(false);
  const { toast } = useToast();

  const fetchCustomers = useCallback(async () => {
    try {
      const response = await getCustomers();

      setCustomers(response.data);

      setIsReady(true);
    } catch (error) {
      if (error instanceof AxiosError) {
        toast({
          variant: 'destructive',
          title: 'Error Fetching Customers',
          description: error.message,
        });
      }
    }
  }, [toast]);

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
