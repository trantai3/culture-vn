// Auth
export const LOGIN_API = "auth/login";

// User
export const PROFILE_API = "users/profile";

// Image
export const UPLOAD_IMAGE = "image-caption/upload";
export const SAVE_CAPTION_IMAGE = (idImage) =>
  `image-caption/caption/${idImage}`;
