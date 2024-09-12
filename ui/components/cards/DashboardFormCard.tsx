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
    <div className="flex items-center justify-center h-full w-full min-w-[750px]">
      <Card className="min-w-[400px] shadow-md">
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
