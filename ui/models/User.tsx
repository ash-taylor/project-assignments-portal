import { ProjectResponse } from './Project';

export enum UserRole {
  MANAGER = 'MANAGER',
  ENGINEER = 'ENGINEER',
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

export interface UserUpdate {
  first_name: string;
  last_name: string;
  email: string;
}

export interface UserCreate extends UserUpdate {
  role: UserRole;
  password: string;
  user_name: string;
  confirm_password: string;
}

export interface UserResponse extends UserUpdate {
  user_name: string;
  role: UserRole;
  id: string;
  admin: boolean;
  active: boolean;
  project_id: string | null;
}

export interface UserLogin {
  username: string;
  password: string;
}
