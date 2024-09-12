import { AxiosError } from 'axios';
import { CircleXIcon, PencilIcon } from 'lucide-react';
import { useContext, useState } from 'react';

import AuthContext from '@/context/AuthContext';
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
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '../ui/hover-card';
import { LoadingSpinner } from '../ui/loading-spinner';

interface CustomerProps {
  customer: CustomerResponse;
  handleRefresh: () => void;
}

const Customer = ({ customer, handleRefresh }: CustomerProps) => {
  const [isReady, setIsReady] = useState<boolean>(true);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);

  const { toast } = useToast();
  const { isAdmin, logout } = useContext(AuthContext);

  const handleDelete = async () => {
    try {
      if (!isAdmin())
        return toast({
          title: 'Error - Cannot Delete Customer!',
          description: 'You must have admin rights to perform this action',
          variant: 'destructive',
        });

      setIsDeleting(true);
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
            return logout();
          }, 2000);
        } else if (error.response?.status === 403) {
          toast({
            title: 'Error - Cannot Delete Customer!',
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
          });
        } else if (error.response?.status === 404) {
          toast({
            title: 'Error - Cannot Delete Customer!',
            description: 'Customer not found!',
            variant: 'destructive',
          });
        } else {
          toast({
            title: 'Error',
            description: 'Something went wrong!',
            variant: 'destructive',
          });
        }
      }
    } finally {
      setIsDeleting(false);
      setIsReady(true);
    }
  };

  return (
    <Card className="m-4">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>{customer.name}</CardTitle>
          <div className="flex gap-2">
            <HoverCard>
              <HoverCardTrigger>
                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" size="icon" disabled={!isAdmin()}>
                      <PencilIcon />
                    </Button>
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
              </HoverCardTrigger>
              {!isAdmin() && (
                <HoverCardContent>
                  <p className="text-sm">Only admins can access this option</p>
                </HoverCardContent>
              )}
            </HoverCard>
            <HoverCard>
              <HoverCardTrigger>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="destructive"
                      size="icon"
                      disabled={!isAdmin()}
                    >
                      {isDeleting ? <LoadingSpinner /> : <CircleXIcon />}
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent>
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                      <AlertDialogDescription>
                        This action cannot be undone. This will permanently
                        delete {customer.name} and any associated projects.
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
                {!isAdmin() && (
                  <HoverCardContent>
                    <p className="text-sm">
                      Only admins can access this option
                    </p>
                  </HoverCardContent>
                )}
              </HoverCardTrigger>
            </HoverCard>
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
