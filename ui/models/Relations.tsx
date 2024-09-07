import { ProjectResponse } from './Project';
import { UserResponse } from './User';

export interface ProjectWithUserResponse extends ProjectResponse {
  users: [UserResponse];
}

export interface UserWithProjectResponse extends UserResponse {
  project: ProjectResponse;
}
