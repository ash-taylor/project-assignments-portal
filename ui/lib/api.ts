import axios from 'axios';

import { CustomerCreate, CustomerResponse } from '@/models/Customer';
import { ProjectCreate, ProjectResponse } from '@/models/Project';
import {
  ProjectWithUserResponse,
  UserWithProjectResponse,
} from '@/models/Relations';
import { UserCreate, UserLogin, UserResponse, UserUpdate } from '@/models/User';

// Login and logout
export const logInUser = async (user: UserLogin) =>
  await axios.post<{}>('/api/login', user, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

export const logOutUser = async () => await axios.post('/api/logout');

// Users CRUD
export const createUser = async (user: UserCreate) =>
  await axios.post<{}>('/api/user', user, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

export const whoAmI = async () =>
  await axios.get<UserWithProjectResponse>('api/users/me', {
    withCredentials: true,
  });

export const getUsers = async (projects?: boolean) => {
  const queryParams = '?projects=true';
  const url = projects ? `api/users${queryParams}` : 'api/users';
  return await axios.get<UserWithProjectResponse[]>(url, {
    headers: { 'Content-Type': 'application/json' },
  });
};

export const updateUser = async (userId: string, user: UserUpdate) =>
  await axios.patch<UserResponse>(`/api/user/${userId}`, user, {
    headers: { 'Content-Type': 'application/json' },
  });

export const assignProjectToUser = async (userId: string, projectId: string) =>
  await axios.patch<UserWithProjectResponse>(
    `/api/user/${userId}/project/${projectId}`,
    {},
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

export const unassignProjectFromUser = async (userId: string) =>
  await axios.patch<UserResponse>(
    `/api/user/${userId}/unassign_project`,
    {},
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

export const deleteUser = async (userId: string) =>
  await axios.delete(`api/user/${userId}`);

// Projects CRUD
export const createProject = async (project: ProjectCreate) =>
  await axios.post<ProjectResponse>('/api/project', project, {
    headers: { 'Content-Type': 'application/json' },
  });

export const getProjects = async (users?: boolean) => {
  const queryParams = '?users=true';
  const url = users ? `api/projects${queryParams}` : 'api/projects';
  return await axios.get<ProjectWithUserResponse[]>(url, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

export const getProjectsWithUsers = async () =>
  await axios.get<ProjectWithUserResponse[]>('api/projects?users=true');

export const updateProject = async (
  projectId: string,
  project: ProjectCreate
) =>
  await axios.put<ProjectResponse>(`/api/project/${projectId}`, project, {
    headers: { 'Content-Type': 'application/json' },
  });

export const deleteProject = async (projectId: string) =>
  await axios.delete(`api/project/${projectId}`);

// Customers CRUD
export const createCustomer = async (customer: CustomerCreate) =>
  await axios.post<CustomerResponse>('/api/customer', customer, {
    headers: { 'Content-Type': 'application/json' },
  });

export const getCustomers = async () =>
  await axios.get<CustomerResponse[]>('api/customers');

export const updateCustomer = async (
  customerId: string,
  customer: CustomerCreate
) =>
  await axios.put<CustomerResponse>(`/api/customer/${customerId}`, customer, {
    headers: { 'Content-Type': 'application/json' },
  });

export const deleteCustomer = async (customerId: string) =>
  await axios.delete(`api/customer/${customerId}`);
