'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/card';

interface DashboardViewCardProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

const DashboardViewCard = ({
  title,
  description,
  children,
}: DashboardViewCardProps) => {
  return (
    <Card className="w-full h-full flex flex-col">
      <CardHeader className="flex-shrink-0">
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent className="flex-grow overflow-auto">{children}</CardContent>
    </Card>
  );
};
export default DashboardViewCard;
