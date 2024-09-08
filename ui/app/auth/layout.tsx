import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Project Assignments Portal - Log In or Create an Account',
};

const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <main className="w-full h-full">
      <div className="h-screen flex items-center justify-center">
        {children}
      </div>
    </main>
  );
};

export default AuthLayout;
