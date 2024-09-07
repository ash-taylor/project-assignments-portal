'use client';

import { Bar, BarChart, CartesianGrid, XAxis } from 'recharts';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { useEffect, useState } from 'react';
import { ProjectWithUserResponse } from '@/models/Relations';
import { getProjectsWithUsers } from '@/lib/api';
import { UserRole } from '@/models/User';
import { LoadingSpinner } from '../ui/loading-spinner';
import { LoadingScreen } from '../ui/loading-screen';

export const description = 'Project engineering effort';

export default function GeneralCard() {
  const [chartData, setChartData] =
    useState<{ project: string; engineers: number }[]>();
  const [isReady, setIsReady] = useState<boolean>(false);

  const chartConfig = {
    engineers: {
      label: 'Engineers',
      color: 'hsl(var(--chart-1))',
    },
  } satisfies ChartConfig;

  useEffect(() => {
    const processChartData = (projects: [ProjectWithUserResponse]) => {
      const data: {
        project: string;
        engineers: number;

        name: string;
      }[] = [];

      projects.forEach((project) => {
        if (project.users)
          data.push({
            project: project.id,
            name: project.name,
            engineers: project.users.filter(
              (user) => user.role === UserRole.ENGINEER
            ).length,
          });
      });

      setChartData(data);
    };

    const fetchProjectsData = async () => {
      const response = await getProjectsWithUsers();

      if (response.status !== 200) {
        console.error('ERROR');
      }

      const projects = response.data;

      processChartData(projects);
    };

    fetchProjectsData();
  }, []);

  useEffect(() => {
    if (chartConfig !== undefined && chartData !== undefined) {
      setIsReady(true);
    }
  }, [chartConfig, chartData, isReady, setIsReady]);

  return (
    <Card className="w-full h-full">
      <CardHeader>
        <CardTitle>Project Assignments</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4 h-[700px]">
        {isReady ? (
          <ChartContainer config={chartConfig} className="h-[650px]">
            <BarChart accessibilityLayer data={chartData}>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="name"
                tickLine={false}
                tickMargin={10}
                axisLine={false}
                tickFormatter={(value) => value.slice(0, 5)}
              />
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent hideLabel />}
              />
              <Bar
                dataKey="engineers"
                fill="var(--color-engineers)"
                radius={8}
              />
            </BarChart>
          </ChartContainer>
        ) : (
          <div className="flex flex-col items-center justify-center">
            <LoadingSpinner message="Loading active project assignments overview..." />
          </div>
        )}
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        {isReady && (
          <>
            <div className="flex items-center gap-2 font-medium leading-none">
              {chartData?.length} projects in flight
            </div>
            <div className="leading-none text-muted-foreground">
              Showing engineer project assignment numbers
            </div>
          </>
        )}
      </CardFooter>
    </Card>
  );
}
