import { UserRole } from '@/models/User';
import { z } from 'zod';

export const RegisterSchema = z
  .object({
    email: z.string().email({ message: 'Please enter a valid email' }),
    user_name: z
      .string()
      .length(8, { message: 'Username must be 8 characters' }),
    first_name: z.string().min(1, 'Please enter your first name'),
    last_name: z.string().min(1, { message: 'Please enter your last name' }),
    role: z.nativeEnum(UserRole, {
      message: 'Role most be either "MANAGER", "ENGINEER" or "CUSTOMER"',
    }),
    password: z
      .string()
      .min(8, { message: 'Password must be at least 8 characters long.' }),
    confirm_password: z
      .string()
      .min(8, { message: 'Password must be at least 8 characters long.' }),
  })
  .refine((values) => values.password === values.confirm_password, {
    message: 'Passwords must match!',
    path: ['confirmPassword'],
  });

export const LoginSchema = z.object({
  username: z.string().length(8, { message: 'Please enter valid username' }),
  password: z
    .string()
    .min(8, { message: 'Password must be at least 8 characters long.' }),
});

export const AddCustomerSchema = z.object({
  name: z
    .string()
    .min(3, { message: 'Customer name must be at least 3 characters' }),
  details: z
    .string()
    .max(100, {
      message: 'Customer details must be a maximum of 100 characters',
    })
    .optional(),
});
