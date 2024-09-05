import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import { AuthProvider } from '@/app/context/AuthContext';

import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Project Assignments Portal',
  description: 'A web application to manage SDE & TPM project assignments',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <AuthProvider>
        <body className={inter.className}>{children}</body>
      </AuthProvider>
    </html>
  );
}
