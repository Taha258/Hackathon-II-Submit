// User Types
export interface User {
  id: string;
  email: string;
  name: string | null;
}

// Auth Types
export interface SignupData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Task Types
export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}