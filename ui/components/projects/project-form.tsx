'use client';

import { AxiosError } from 'axios';
import { zodResolver } from '@hookform/resolvers/zod';
import { CaretSortIcon, CheckIcon } from '@radix-ui/react-icons';
import { useCallback, useContext, useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { useToast } from '@/hooks/use-toast';
import { createProject, getCustomers, updateProject } from '@/lib/api';
import { cn } from '@/lib/utils';
import { CustomerResponse } from '@/models/Customer';
import { ProjectStatus } from '@/models/Project';
import { AddProjectSchema } from '@/schema';
import { Button, ButtonLoading } from '../ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '../ui/command';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import { Input } from '../ui/input';
import { LoadingSpinner } from '../ui/loading-spinner';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import AuthContext from '@/context/AuthContext';

interface AddProjectFormProps {
  formType: 'add';
}

interface EditProjectFormProps {
  formType: 'edit';
  projectId: string;
  projectName: string;
  projectDetails?: string;
  projectStatus: string;
  customerId: string;
  handleRefresh: () => void;
}

type ProjectFormProps = AddProjectFormProps | EditProjectFormProps;

const ProjectForm = (props: ProjectFormProps) => {
  const [customers, setCustomers] = useState<CustomerResponse[] | undefined>(
    undefined
  );
  const [isReady, setIsReady] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const { toast } = useToast();
  const { logout } = useContext(AuthContext);

  const form = useForm({
    resolver: zodResolver(AddProjectSchema),
    defaultValues: {
      name: props.formType === 'edit' ? props.projectName : '',
      details: props.formType === 'edit' ? props.projectDetails || '' : '',
      status:
        props.formType === 'edit'
          ? (props.projectStatus as ProjectStatus)
          : ProjectStatus.PENDING,
      customer_id: props.formType === 'edit' ? props.customerId : '',
    },
  });

  const handleSubmit = async (data: z.infer<typeof AddProjectSchema>) => {
    setIsLoading(true);
    try {
      if (props.formType === 'edit') {
        await updateProject(props.projectId, data);
      } else {
        await createProject(data);
      }

      toast({
        title: 'Success',
        description: `Project successfully ${
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
        } else if (error.response?.status === 409) {
          toast({
            title: 'Error - Cannot Update Project!',
            description: `Project ${
              props.formType === 'edit' ? 'name' : ''
            } already exists!`,
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
      form.reset();
      setIsLoading(false);
    }
  };

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
          }, 2000);
        } else {
          toast({
            variant: 'destructive',
            title: 'Error Fetching Customers. Try again later...',
            description: error.message,
          });
        }
      }
    }
  }, [logout, toast]);

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  return (
    <>
      {isReady ? (
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="space-y-6"
          >
            <div className="space-y-4">
              <FormField
                control={form.control}
                name="customer_id"
                render={({ field }) => (
                  <FormItem className="flex flex-col">
                    <FormLabel>Customer</FormLabel>
                    <Popover>
                      <PopoverTrigger asChild>
                        <FormControl>
                          <Button
                            variant="outline"
                            role="combobox"
                            className={cn(
                              'justify-between',
                              !field.value && 'text-muted-foreground'
                            )}
                          >
                            {field.value
                              ? customers!.find(
                                  (customer) => customer.id === field.value
                                )?.name
                              : 'Select Customer'}
                            <CaretSortIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                          </Button>
                        </FormControl>
                      </PopoverTrigger>
                      <PopoverContent className="p-0">
                        <Command>
                          <CommandInput
                            placeholder="Search customer..."
                            className="h-9"
                          />
                          <CommandList>
                            <CommandEmpty>No customer found.</CommandEmpty>
                            <CommandGroup>
                              {customers!.map((customer) => (
                                <CommandItem
                                  value={customer.name}
                                  key={customer.id}
                                  onSelect={() => {
                                    form.setValue('customer_id', customer.id);
                                  }}
                                >
                                  {customer.name}
                                  <CheckIcon
                                    className={cn(
                                      'ml-auto h-4 w-4',
                                      customer.id === field.value
                                        ? 'opacity-100'
                                        : 'opacity-0'
                                    )}
                                  />
                                </CommandItem>
                              ))}
                            </CommandGroup>
                          </CommandList>
                        </Command>
                      </PopoverContent>
                    </Popover>
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Project Name</FormLabel>
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
                    <FormLabel>Project Details</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        type="text"
                        placeholder={
                          props.formType === 'add' || !props.projectDetails
                            ? 'Project details (optional)'
                            : undefined
                        }
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Project Status</FormLabel>
                    <Select
                      onValueChange={(value) =>
                        field.onChange(value as ProjectStatus)
                      }
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a status" />
                        </SelectTrigger>
                      </FormControl>
                      <FormMessage />
                      <SelectContent>
                        {Object.values(ProjectStatus).map((status, idx) => (
                          <SelectItem key={idx} value={status}>
                            {status}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </FormItem>
                )}
              />
            </div>
            {isLoading ? (
              <ButtonLoading
                message={`${
                  props.formType === 'add' ? 'Creating new' : 'Updating'
                } Project...`}
              />
            ) : (
              <Button type="submit" className="w-full">
                {props.formType === 'add' ? 'Add ' : 'Update '}Project
              </Button>
            )}
          </form>
        </Form>
      ) : (
        <div className="flex items-center justify-center h-full w-full">
          <LoadingSpinner message="Loading form data..." />
        </div>
      )}
    </>
  );
};
export default ProjectForm;
