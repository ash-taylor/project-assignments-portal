'use client';

import { AddCustomerSchema } from '@/schema';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import { Input } from '../ui/input';

import { Button, ButtonLoading } from '../ui/button';
import { createCustomer, updateCustomer } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { AxiosError } from 'axios';

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

      form.reset();

      if (props.formType === 'edit') props.handleRefresh();
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response?.status === 409) {
          toast({
            title: 'Error - Cannot Update Customer!',
            description: 'Customer already exists!',
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
      form.reset();
      console.error(error);
    }

    setIsLoading(false);
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
