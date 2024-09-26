import pkg from '@next/env';
import { configDotenv } from 'dotenv';
import path from 'path';

const { loadEnvConfig } = pkg;

const envDir = path.resolve(process.cwd(), '../');

loadEnvConfig(envDir);
configDotenv({ path: envDir });
