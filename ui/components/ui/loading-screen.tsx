import { LoadingSpinner } from './loading-spinner';

interface LoadingScreenProps {
  message: string;
}

export const LoadingScreen = ({ message }: LoadingScreenProps) => (
  <div className="min-h-screen flex flex-col items-center justify-center">
    <LoadingSpinner className="p-3 m-5" />
    <p className="text-base text-muted-foreground">{message}</p>
  </div>
);
