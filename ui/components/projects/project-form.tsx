'use client';

import { AddCustomerSchema, AddProjectSchema } from '@/schema';
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
import { ProjectStatus } from '@/models/Project';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';

interface AddFormProps {
  formType: 'add';
}

interface EditFormProps {
  formType: 'edit';
  projectId: string;
  projectName: string;
  projectDetails?: string;
  projectStatus: string;
  customerId: string;
  handleRefresh: () => void;
}

type ProjectFormProps = AddFormProps | EditFormProps;

const ProjectForm = (props: ProjectFormProps) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const { toast } = useToast();

  const form = useForm({
    resolver: zodResolver(AddProjectSchema),
    defaultValues: {
      name: props.formType === 'edit' ? props.projectName : '',
      details: props.formType === 'edit' ? props.projectDetails || '' : '',
      status:
        props.formType === 'edit' ? props.projectStatus : ProjectStatus.PENDING,
      cutomer_id: props.formType === 'edit' ? props.customerId : undefined,
    },
  });

  const handleSubmit = async (data: z.infer<typeof AddCustomerSchema>) => {
    setIsLoading(true);
    try {
      if (props.formType === 'edit') {
        await updateCustomer(props.projectId, data);
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
                      <SelectValue placeholder="Select a role" />
                    </SelectTrigger>
                  </FormControl>
                  <FormMessage />
                  <SelectContent>
                    {Object.keys(ProjectStatus).map((key, idx) => (
                      <SelectItem
                        key={idx}
                        value={ProjectStatus[key as ProjectStatus]}
                      >
                        {ProjectStatus[key as ProjectStatus]}
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
export default ProjectForm;
