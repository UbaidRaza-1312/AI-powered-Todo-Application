// frontend/src/services/userService.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://ubaidraza1565-ai-todo.hf.space';

interface UserProfileWithStats {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
}

class UserService {
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  async getUserProfileWithStats(): Promise<UserProfileWithStats> {
    const response = await fetch(`${API_BASE_URL}/api/auth/profile`, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      const text = await response.text();

      let message = 'Failed to get user profile';
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
}

export default new UserService();
export type { UserProfileWithStats };