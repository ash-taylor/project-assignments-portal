export interface CustomerResponse {
  name: string;
  details?: string;
  id: string;
  active: boolean;
}

export interface CustomerCreate {
  name: string;
  details?: string;
}
