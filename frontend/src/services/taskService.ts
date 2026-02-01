// frontend/src/services/taskService.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://ubaidraza1565-ai-todo.hf.space';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
  due_date?: string;
}

interface TaskCreateData {
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
}

interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
}

class TaskService {
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

  async getTasks(completed?: boolean): Promise<Task[]> {
    let url = `${API_BASE_URL}/api/tasks`;
    if (completed !== undefined) {
      url += `?completed=${completed}`;
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch tasks: ${response.statusText}`);
    }

    return response.json();
  }

  async createTask(taskData: TaskCreateData): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to create task: ${response.statusText}`);
    }

    return response.json();
  }

  async getTaskById(taskId: string): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'GET',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch task: ${response.statusText}`);
    }

    return response.json();
  }

  async updateTask(taskId: string, taskData: TaskUpdateData): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`Failed to update task: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteTask(taskId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to delete task: ${response.statusText}`);
    }
  }

  async toggleTaskCompletion(taskId: string): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error(`Failed to toggle task completion: ${response.statusText}`);
    }

    return response.json();
  }
}

export default new TaskService();
export type { Task, TaskCreateData, TaskUpdateData };