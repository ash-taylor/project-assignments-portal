'use client';

import { Button } from '@/components/ui/button';
import { getHelloWorld } from './util/apis';

export default function Home() {
  async function handleClick() {
    const res = await getHelloWorld();

    console.log(res);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Button onClick={handleClick}>Log in</Button>
    </main>
  );
}
