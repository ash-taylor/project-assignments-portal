'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';

interface DashboardFormCardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

const DashboardFormCard = ({
  title,
  description,
  children,
}: DashboardFormCardProps) => {
  return (
    <div className="flex items-center justify-center h-full w-full">
      <Card className="xl:w-1/4 md:w-1/2 shadow-md">
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
        <CardContent className="flex-grow overflow-auto">
          {children}
        </CardContent>
      </Card>
    </div>
  );
};
export default DashboardFormCard;
