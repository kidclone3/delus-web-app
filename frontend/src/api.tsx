const baseUrl: string | undefined = process.env.APP_API;

export const api: { [key: string]: any } = {};

api.get = async (endpoint: string): Promise<any> => {
  const res = await fetch(`${baseUrl}${endpoint}`);
  if (res.json) return (await res.json()) || [];
  return res;
};
