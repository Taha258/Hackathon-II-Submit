// 📁 Location: frontend/src/components/AuthWrapper.tsx

'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Public routes that don't need authentication
  const publicRoutes = ['/', '/login', '/signup'];

  useEffect(() => {
    const token = localStorage.getItem('token');
    const isPublicRoute = publicRoutes.includes(pathname);

    if (!token && !isPublicRoute) {
      // Not authenticated and trying to access protected route
      router.push('/login');
    } else if (token && (pathname === '/login' || pathname === '/signup')) {
      // Authenticated and trying to access login/signup
      router.push('/dashboard');
    } else {
      setIsAuthenticated(true);
    }

    setLoading(false);
  }, [pathname, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-secondary/20 to-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}