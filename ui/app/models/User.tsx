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

export interface ProjectResponse {
  name: string;
  status: string;
  details: string;
  customer_id: string;
  id: string;
}

export interface UserResponse {
  user_name: string;
  first_name: string;
  last_name: string;
  role: string;
  email: string;
  id: string;
  admin: boolean;
  active: boolean;
  project_id: string | null;
  project: ProjectResponse | null;
}
