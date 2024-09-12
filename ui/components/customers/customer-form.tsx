'use client';

import { AxiosError } from 'axios';
import { useContext, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { createCustomer, updateCustomer } from '@/lib/api';
import { AddCustomerSchema } from '@/schema';
import { Button, ButtonLoading } from '../ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import { Input } from '../ui/input';

interface AddCustomerFormProps {
  formType: 'add';
}

interface EditCustomerFormProps {
  formType: 'edit';
  customerId: string;
  customerName: string;
  customerDetails?: string;
  handleRefresh: () => void;
}

type CustomerFormProps = AddCustomerFormProps | EditCustomerFormProps;

const CustomerForm = (props: CustomerFormProps) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const { toast } = useToast();
  const { isAdmin, logout } = useContext(AuthContext);

  const errorTitle = `Error - Cannot ${
    props.formType === 'add' ? 'Add' : 'Update'
  } Customer!`;

  const form = useForm({
    resolver: zodResolver(AddCustomerSchema),
    defaultValues: {
      name: props.formType === 'edit' ? props.customerName : '',
      details: props.formType === 'edit' ? props.customerDetails || '' : '',
    },
  });

  const handleSubmit = async (data: z.infer<typeof AddCustomerSchema>) => {
    setIsLoading(true);
    try {
      if (!isAdmin())
        return toast({
          title: errorTitle,
          description: 'You must have admin rights to perform this action',
          variant: 'destructive',
        });

      if (props.formType === 'edit') {
        await updateCustomer(props.customerId, data);
      } else {
        await createCustomer(data);
      }

      toast({
        title: 'Success',
        description: `Customer successfully ${
          props.formType === 'edit' ? 'updated' : 'added to the system'
        }`,
      });

      if (props.formType === 'edit') props.handleRefresh();
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
            title: errorTitle,
            description: 'You must have admin rights to perform this action',
            variant: 'destructive',
          });
        } else if (error.response?.status === 404) {
          toast({
            title: errorTitle,
            description: 'Customer not found!',
            variant: 'destructive',
          });
        } else if (error.response?.status === 409) {
          toast({
            title: errorTitle,
            description: `Customer ${
              props.formType === 'edit' ? 'name' : ''
            } already exists!`,
            variant: 'destructive',
          });
        } else {
          toast({
            title: errorTitle,
            description: 'Something went wrong!',
            variant: 'destructive',
          });
        }
      }
    } finally {
      form.reset();
      setIsLoading(false);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <div className="space-y-4">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Customer Name</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    placeholder={
                      props.formType === 'add' ? 'Amazon' : undefined
                    }
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="details"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Customer Details</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="text"
                    placeholder={
                      props.formType === 'add' || !props.customerDetails
                        ? 'Customer details (optional)'
                        : undefined
                    }
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        {isLoading ? (
          <ButtonLoading
            message={`${
              props.formType === 'add' ? 'Creating new' : 'Updating'
            } customer...`}
          />
        ) : (
          <Button type="submit" className="w-full">
            {props.formType === 'add' ? 'Add ' : 'Update '}Customer
          </Button>
        )}
      </form>
    </Form>
  );
};
export default CustomerForm;
