import './envConfig.mjs';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  rewrites: async () => {
    if (process.env.ENVIRONMENT === 'development') {
      return [
        {
          source: '/api/:path*',
          destination: 'http://127.0.0.1:8000/api/:path*',
        },
        {
          source: '/docs',
          destination: 'http://127.0.0.1:8000/docs',
        },
        {
          source: '/openapi.json',
          destination: 'http://127.0.0.1:8000/openapi.json',
        },
      ];
    } else {
      return [];
    }
  },
};

export default nextConfig;
