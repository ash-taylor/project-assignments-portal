export enum ProjectStatus {
  PENDING = 'PENDING',
}

export interface ProjectResponse {
  name: string;
  status: ProjectStatus;
  details: string;
  customer_id: string;
  id: string;
  customer: CustomerResponse;
}
