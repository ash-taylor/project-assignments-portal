'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useContext, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import CardWrapper from '@/components/auth/card-wrapper';
import { Button, ButtonLoading } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import AuthContext from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { LoginSchema } from '@/schema';

const LoginForm = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const { login } = useContext(AuthContext);
  const { toast } = useToast();

  const form = useForm({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  });

  const handleLogin = async (data: z.infer<typeof LoginSchema>) => {
    setIsLoading(true);
    const response = await login(data);

    if (response?.status === 401) {
      toast({
        title: 'Error',
        description: 'Invalid username or password',
        variant: 'destructive',
      });
      form.reset();
    } else if (response?.status !== 204) {
      toast({
        title: 'Error',
        description: 'Unable to log in user',
        variant: 'destructive',
      });
      form.reset();
    }

    setIsLoading(false);
  };

  return (
    <CardWrapper
      label="Log in to your account"
      title="Log In"
      backButtonHref="/auth/register"
      backButtonLabel="Don't have an account? Register here."
    >
      <Form {...form}>
        <form onSubmit={form.handleSubmit(handleLogin)} className="space-y-6">
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="username"
                      autoComplete="username"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="********"
                      type="password"
                      autoComplete="new-password"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          {isLoading ? (
            <ButtonLoading message="Logging in user..." />
          ) : (
            <Button type="submit" className="w-full">
              Log In
            </Button>
          )}
        </form>
      </Form>
    </CardWrapper>
  );
};

export default LoginForm;
