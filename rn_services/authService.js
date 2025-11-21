import API from './api';

export const register = async (data) => {
  const res = await API.post('/auth/register/', data);
  return res.data;
};

export const login = async (data) => {
  const res = await API.post('/auth/login/', data);
  return res.data;
};
