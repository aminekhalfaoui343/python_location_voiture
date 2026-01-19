import { useState } from 'react';

/**
 * Hook personnalisé pour gérer l'upload d'images
 */
export const useImageUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const uploadImage = async (carId, file) => {
    if (!file) {
      setError('Please select an image');
      return null;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be less than 5MB');
      return null;
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Allowed formats: JPG, PNG, GIF, WebP');
      return null;
    }

    try {
      setUploading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`/api/images/cars/${carId}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      return data;
    } catch (err) {
      const errorMessage = err.message || 'Failed to upload image';
      setError(errorMessage);
      return null;
    } finally {
      setUploading(false);
    }
  };

  const deleteImage = async (carId) => {
    try {
      setUploading(true);
      setError(null);

      const response = await fetch(`/api/images/cars/${carId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Delete failed');

      return true;
    } catch (err) {
      setError(err.message || 'Failed to delete image');
      return false;
    } finally {
      setUploading(false);
    }
  };

  return {
    uploading,
    error,
    uploadImage,
    deleteImage,
    setError,
  };
};

export default useImageUpload;
