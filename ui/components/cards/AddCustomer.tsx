'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';

interface AddCustomerCardProps {
  children: React.ReactNode;
}

const AddCustomerCard = ({ children }: AddCustomerCardProps) => {
  return (
    <Card className="w-full h-full">
      <CardHeader>
        <CardTitle>Add Customer</CardTitle>
        <CardDescription>Add a new customer to the portal</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 h-[700px]">{children}</CardContent>
    </Card>
  );
};
export default AddCustomerCard;
