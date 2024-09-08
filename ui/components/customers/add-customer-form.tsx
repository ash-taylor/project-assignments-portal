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
import { createCustomer } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

const AddCustomerForm = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { toast } = useToast();

  const form = useForm({
    resolver: zodResolver(AddCustomerSchema),
    defaultValues: {
      name: '',
      details: '',
    },
  });

  const handleAdd = async (data: z.infer<typeof AddCustomerSchema>) => {
    setIsLoading(true);
    try {
      await createCustomer(data);
      form.reset();
      toast({
        title: 'Success',
        description: 'Customer added to the system',
      });
    } catch (error) {
      console.error(error);
    }

    setIsLoading(false);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleAdd)} className="space-y-6">
        <div className="space-y-4">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Customer Name</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="Amazon" />
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
                    placeholder="Customer details (optional)"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        {isLoading ? (
          <ButtonLoading message="Creating new customer..." />
        ) : (
          <Button type="submit" className="w-full">
            Add a customer
          </Button>
        )}
      </form>
    </Form>
  );
};
export default AddCustomerForm;
