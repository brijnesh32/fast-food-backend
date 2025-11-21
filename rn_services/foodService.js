import API from './api';

export const getFoods = async () => {
  const res = await API.get('/foods/');
  return res.data;
};

export const createFood = async (data) => {
  const res = await API.post('/foods/create/', data);
  return res.data;
};
