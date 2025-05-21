import api from '../services/axios';

export const login = async (username, password) => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  return api.post('/auth/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};

export const register = async (email, username, password) => {
  return api.post('/users/create', {
    email,
    username,
    password,
  });
}; 