export async function getHelloWorld() {
  const response = await fetch('/api/python');

  return await response.json();
}
