import { CustomerCreate, CustomerResponse } from '@/models/Customer';
import {
  ProjectWithUserResponse,
  UserWithProjectResponse,
} from '@/models/Relations';
import { UserCreate, UserLogin } from '@/models/User';
import axios from 'axios';

export const whoAmI = async () =>
  await axios.get<UserWithProjectResponse>('api/users/me', {
    withCredentials: true,
  });

export const createUser = async (user: UserCreate) =>
  await axios.post<{}>('/api/user', user, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

export const logInUser = async (user: UserLogin) =>
  await axios.post<{}>('/api/login', user, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

export const logOutUser = async () => await axios.post('/api/logout');

export const getProjectsWithUsers = async () =>
  await axios.get<[ProjectWithUserResponse]>('api/projects?users=true');

export const createCustomer = async (customer: CustomerCreate) =>
  await axios.post<CustomerResponse>('/api/customer', customer, {
    headers: { 'Content-Type': 'application/json' },
  });
