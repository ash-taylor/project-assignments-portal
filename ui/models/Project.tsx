import { CustomerResponse } from './Customer';

export enum ProjectStatus {
  PENDING = 'PENDING',
  DESIGN = 'DESIGN',
  BUILD = 'BUILD',
  COMPLETE = 'COMPLETE',
}

export interface ProjectResponse {
  name: string;
  status: ProjectStatus;
  details: string;
  customer_id: string;
  id: string;
  customer: CustomerResponse;
}
