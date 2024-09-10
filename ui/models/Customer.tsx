export interface CustomerCreate {
  name: string;
  details?: string;
}

export interface CustomerResponse extends CustomerCreate {
  id: string;
  active: boolean;
}
