const cache = new Map<string, string>();

export function useStatic() {
  const apiHost = import.meta.env.VITE_API_HOST;

  const getStaticUrl = (path: string) => {
    if (cache.has(path)) {
      return cache.get(path)!;
    }
    const url = `${apiHost}/static/${path}`;
    cache.set(path, url);
    return url;
  };

  const preloadImage = async (path: string): Promise<void> => {
    const url = getStaticUrl(path);
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve();
      img.onerror = reject;
      img.src = url;
    });
  };

  return {
    getStaticUrl,
    preloadImage,
  };
}
