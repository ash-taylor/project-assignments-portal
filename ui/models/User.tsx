import { ProjectResponse } from './Project';

export enum UserRole {
  MANAGER = 'MANAGER',
  ENGINEER = 'ENGINEER',
  CUSTOMER = 'CUSTOMER',
}

export class User {
  constructor(
    public active: boolean,
    public id: string,
    public username: string,
    public firstName: string,
    public lastName: string,
    public admin: boolean,
    public role: string,
    public email: string,
    public projectId: string | null,
    public project: ProjectResponse | null
  ) {}
}

export interface UserResponse {
  user_name: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  email: string;
  id: string;
  admin: boolean;
  active: boolean;
  project_id: string | null;
}

export interface UserCreate {
  role: UserRole;
  email: string;
  password: string;
  user_name: string;
  first_name: string;
  last_name: string;
  confirm_password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}
