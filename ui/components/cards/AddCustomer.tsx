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
    <div className="flex items-center justify-center h-full w-full">
      <Card className="xl:w-1/4 md:w-1/2 shadow-md">
        <CardHeader>
          <CardTitle>Add Customer</CardTitle>
          <CardDescription>Add a new customer to the portal</CardDescription>
        </CardHeader>
        <CardContent className="">{children}</CardContent>
      </Card>
    </div>
  );
};
export default AddCustomerCard;
