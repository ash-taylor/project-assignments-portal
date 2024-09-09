'use client';

import { useEffect, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from 'recharts';

import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '../ui/chart';
import { ProjectWithUserResponse } from '@/models/Relations';
import { UserRole } from '@/models/User';
import { getProjectsWithUsers } from '@/lib/api';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '../ui/card';
import { LoadingSpinner } from '../ui/loading-spinner';
import CustomXAxisTickWrapper from './TickWrapper';

const ProjectsChart = () => {
  const [chartData, setChartData] =
    useState<{ project: string; engineers: number }[]>();
  const [isReady, setIsReady] = useState<boolean>(false);

  const description = 'Project engineering effort';

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
    <Card className="w-full h-full flex flex-col">
      <CardHeader className="flex-shrink-0">
        <CardTitle>Project Assignments</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-grow overflow-auto">
        {isReady ? (
          <ChartContainer
            config={chartConfig}
            className="h-full w-full min-w-[600px]"
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
              >
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="name"
                  tickLine={false}
                  tickMargin={10}
                  axisLine={false}
                  tick={CustomXAxisTickWrapper}
                  interval={0}
                />
                <YAxis />
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
            </ResponsiveContainer>
          </ChartContainer>
        ) : (
          <div className="flex items-center justify-center h-full w-full">
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
};
export default ProjectsChart;
