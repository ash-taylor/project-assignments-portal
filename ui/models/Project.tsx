import { CustomerResponse } from './Customer';

export enum ProjectStatus {
  PENDING = 'PENDING',
  DESIGN = 'DESIGN',
  BUILD = 'BUILD',
  COMPLETE = 'COMPLETE',
}

export interface ProjectCreate {
  name: string;
  status: ProjectStatus;
  details?: string;
  customer_id: string;
}

export interface ProjectResponse extends ProjectCreate {
  id: string;
  customer: CustomerResponse;
}
