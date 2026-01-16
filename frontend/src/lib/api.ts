// frontend/src/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// -------------------- Helpers --------------------
const getAuthToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

const getUser = () => {
  if (typeof window !== 'undefined') {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
  return null;
};

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  console.log('🔗 API Call:', `${API_URL}${endpoint}`);
  console.log('📤 Request body:', options.body);

  const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    console.error('❌ API Error:', error);
    throw new Error(error.detail || 'API request failed');
  }

  const data = await response.json();
  console.log('✅ API Response:', data);
  return data;
}

// ==================== Auth APIs ====================
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await fetchAPI('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    return {
      token: response.access_token || response.token,
      user: response.user,
    };
  },

  signup: async (email: string, password: string, name?: string) => {
    const response = await fetchAPI('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });

    return {
      token: response.access_token || response.token,
      user: response.user,
    };
  },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },
};

// ==================== Task APIs ====================
export const taskAPI = {
  getTasks: async () => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');
    const data = await fetchAPI(`/api/${user.id}/tasks`);
    return Array.isArray(data) ? data : [];
  },

  getTask: async (id: string) => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');
    return fetchAPI(`/api/${user.id}/tasks/${id}`);
  },

  createTask: async (taskData: {
    title: string;
    description?: string;
    status?: 'todo' | 'in-progress' | 'completed';
    priority?: 'low' | 'medium' | 'high';
    dueDate?: string;
  }) => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');

    return fetchAPI(`/api/${user.id}/tasks`, {
      method: 'POST',
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description || '',
        status: taskData.status || 'todo',
        priority: taskData.priority || 'medium',
        due_date: taskData.dueDate || undefined,
      }),
    });
  },

  updateTask: async (
    id: string,
    taskData: Partial<{
      title: string;
      description: string;
      status: 'todo' | 'in-progress' | 'completed';
      priority: 'low' | 'medium' | 'high';
      dueDate: string;
      completed: boolean;
    }>
  ) => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');

    const payload: any = {};
    if (taskData.title !== undefined) payload.title = taskData.title;
    if (taskData.description !== undefined) payload.description = taskData.description;
    if (taskData.status !== undefined) payload.status = taskData.status;
    if (taskData.priority !== undefined) payload.priority = taskData.priority;
    if (taskData.dueDate !== undefined) payload.due_date = taskData.dueDate;
    if (taskData.completed !== undefined) payload.completed = taskData.completed;

    return fetchAPI(`/api/${user.id}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  },

  toggleComplete: async (id: string) => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');

    return fetchAPI(`/api/${user.id}/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  },

  deleteTask: async (id: string) => {
    const user = getUser();
    if (!user?.id) throw new Error('User not authenticated');

    return fetchAPI(`/api/${user.id}/tasks/${id}`, { method: 'DELETE' });
  },
};

export default { authAPI, taskAPI };
