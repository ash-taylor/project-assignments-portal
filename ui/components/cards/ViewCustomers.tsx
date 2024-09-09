'use client';

import { useCallback, useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { CustomerResponse } from '@/models/Customer';
import { getCustomers } from '@/lib/api';
import Customer from '../customers/customer';
import { LoadingSpinner } from '../ui/loading-spinner';
import { AxiosError } from 'axios';
import { useToast } from '@/hooks/use-toast';

const ViewCustomersCard = () => {
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
    <Card className="w-full h-full flex flex-col">
      <CardHeader className="flex-shrink-0">
        <CardTitle>View Customers</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow overflow-auto">
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
      </CardContent>
    </Card>
  );
};
export default ViewCustomersCard;
