// frontend/src/services/authService.ts

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'https://ubaidraza1565-ai-todo.hf.space';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

interface UserRegistrationData {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

interface UserLoginData {
  email: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  // ================== TOKEN ==================
  private storeToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
      // Also set as a cookie for server-side access (middleware)
      document.cookie = `access_token=${token}; path=/; SameSite=Lax`;
    }
  }

  private removeToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      // Also remove the cookie
      document.cookie = 'access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
  }

  public getToken(): string | null {
    if (typeof window !== 'undefined') {
      // First try to get from localStorage
      const token = localStorage.getItem('access_token');
      if (token) {
        return token;
      }
      // Fallback to cookies if not in localStorage
      return this.getCookie('access_token');
    }
    return null;
  }

  private getCookie(name: string): string | null {
    if (typeof document === 'undefined') return null;

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  }

  // ================== HEADERS ==================
  private getHeaders(): HeadersInit {
    return {
      'Content-Type': 'application/json',
    };
  }

  // ================== REGISTER ==================
  async register(userData: UserRegistrationData): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const text = await response.text();

        let message = 'Registration failed';
        try {
          const data = JSON.parse(text);
          message = data.detail || message;
        } catch {
          message = text;
        }

        throw new Error(message);
      }

      return await response.json();
    } catch (error: any) {
      console.error('REGISTER ERROR:', error.message);
      throw error;
    }
  }

  // ================== LOGIN ==================
  async login(credentials: UserLoginData): Promise<TokenResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const text = await response.text();

        let message = 'Login failed';
        try {
          const data = JSON.parse(text);
          message = data.detail || message;
        } catch {
          message = text;
        }

        throw new Error(message);
      }

      const tokenData: TokenResponse = await response.json();
      this.storeToken(tokenData.access_token);
      return tokenData;
    } catch (error: any) {
      console.error('LOGIN ERROR:', error.message);
      throw error;
    }
  }

  // ================== LOGOUT ==================
  async logout(): Promise<void> {
    try {
      // Call the backend logout endpoint
      const token = this.getToken();
      if (token) {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout endpoint error:', error);
      // Continue with local token removal even if backend call fails
    } finally {
      // Remove token from both localStorage and cookies
      this.removeToken();
    }
  }

  // ================== CURRENT USER ==================
  async getCurrentUser(): Promise<User> {
    const token = this.getToken();
    if (!token) throw new Error('No authentication token found');

    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      method: 'GET',
      headers: {
        ...this.getHeaders(),
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const text = await response.text();

      let message = 'Failed to get user';
      try {
        const data = JSON.parse(text);
        message = data.detail || message;
      } catch {
        message = text;
      }

      throw new Error(message);
    }

    return await response.json();
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}

export default new AuthService();
export type { User, UserRegistrationData, UserLoginData, TokenResponse };
