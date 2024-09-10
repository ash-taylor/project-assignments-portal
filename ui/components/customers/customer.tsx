import { AxiosError } from 'axios';
import { CircleXIcon, PencilIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import CustomerForm from './customer-form';
import { useToast } from '@/hooks/use-toast';
import { deleteCustomer } from '@/lib/api';
import { CustomerResponse } from '@/models/Customer';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '../ui/alert-dialog';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';

interface CustomerProps {
  customer: CustomerResponse;
  handleRefresh: () => void;
}

const Customer = ({ customer, handleRefresh }: CustomerProps) => {
  const [isReady, setIsReady] = useState<boolean>(true);

  const { toast } = useToast();
  const router = useRouter();

  const handleDelete = async () => {
    try {
      setIsReady(false);
      await deleteCustomer(customer.id);
      toast({
        title: 'Success',
        description: `${customer.name} and associated projects successfully deleted`,
      });
      handleRefresh();
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          toast({
            title: 'Session Expired',
            description: 'Your credentials have expired, you must log in again',
            variant: 'destructive',
          });
          setTimeout(() => {
            return router.push('/auth/login');
          }, 3000);
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Deleting Customer',
            description: error.message,
          });
        }
      }
    }
  };
  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{customer.name}</CardTitle>
          <div className="flex gap-2">
            <Dialog>
              <DialogTrigger>
                <PencilIcon />
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit Customer</DialogTitle>
                  <DialogDescription>
                    Make changes to the customer here
                  </DialogDescription>
                </DialogHeader>
                <CustomerForm
                  formType="edit"
                  customerId={customer.id}
                  customerName={customer.name}
                  customerDetails={customer.details}
                  handleRefresh={handleRefresh}
                />
              </DialogContent>
            </Dialog>
            <AlertDialog>
              <AlertDialogTrigger>
                <CircleXIcon />
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete{' '}
                    {customer.name} and any associated projects.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleDelete}>
                    Continue
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        {isReady ? customer.details : 'Deleting customer...'}
      </CardContent>
    </Card>
  );
};

export default Customer;
