import API from './api';

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await API.post('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};
