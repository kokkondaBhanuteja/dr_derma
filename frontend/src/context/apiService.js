import API_BASE_URL from "../config";
/**
 * API Service for Dr. Derma application
 * Provides methods for interacting with backend endpoints
 */

// Get JWT token from localStorage
const getToken = () => sessionStorage.getItem("token");

// Handle API responses consistently
const handleResponse = async (response) => {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    console.error(`❌ API Error (${response.status}):`, data);

    if (response.status === 400) {
      throw new Error(data.error || "Bad Request - Check input data");
    }
    if (response.status === 401) {
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("user");
      window.location.href = "/login";
      throw new Error("Session expired. Please log in again.");
    }
    throw new Error(data.error || "An unknown error occurred.");
  }

  return data;
};

// Create headers with authentication if token exists
const createHeaders = (
  contentType = "application/json",
  includeAuth = true
) => {
  const headers = {
    "Content-Type": contentType,
  };

  const token = getToken();
  if (token && includeAuth) {
    headers["Authorization"] = `Bearer ${token}`;
  } else if (includeAuth) {
    console.warn(
      "🚨 No token found! Request may fail due to missing authentication."
    );
  }

  console.log("🛠️ Generated Headers:", headers); // Debugging log

  return headers;
};

// API methods
const apiService = {
  // Auth endpoints
  async register(userData) {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: createHeaders(),
      body: JSON.stringify(userData),
    });

    return handleResponse(response);
  },

  async login(credentials) {
    console.log("🔍 Sending login request with:", credentials); // Debugging

    if (!credentials || !credentials.email || !credentials.password) {
      console.error("❌ Login failed: Missing email or password");
      throw new Error("Email and password are required");
    }

    console.log("🔍 Sending login request with:", credentials); // Debugging

    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: createHeaders(),
      body: JSON.stringify(credentials),
    });

    return handleResponse(response);
  },

  async getCurrentUser() {
    const response = await fetch("/api/auth/me", {
      method: "GET",
      headers: createHeaders(),
    });

    return handleResponse(response);
  },

  // Profile endpoints
  async getProfile() {
    const response = await fetch("/api/profile", {
      method: "GET",
      headers: createHeaders(),
    });

    return handleResponse(response);
  },

  async updateProfile(profileData) {
    const response = await fetch("/api/profile", {
      method: "PUT",
      headers: createHeaders(),
      body: JSON.stringify(profileData),
    });

    return handleResponse(response);
  },

  // Image analysis endpoints
  async uploadAndAnalyzeImage(imageFile) {
    const formData = new FormData();
    formData.append("image", imageFile);

    const response = await fetch("/api/analysis/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${getToken()}`,
        // Note: Don't set Content-Type for FormData
      },
      body: formData,
    });

    return handleResponse(response);
  },

  async getUserImages() {
    const response = await fetch("/api/analysis/images", {
      method: "GET",
      headers: createHeaders(),
    });

    return handleResponse(response);
  },

  async analyzeSkinFromQuestionnaire(skinData) {
    console.log("🔍 Sending request with token:", getToken());

    // Add the missing subject field
    const dataWithSubject = {
      ...skinData,
      subject: typeof skinData.subject === 'string' ? skinData.subject : "Skin Analysis"
    };

    console.log("📤 Sending data:", JSON.stringify(dataWithSubject));

    const analyzeResponse = await fetch(
      `/api/analysis/analyze-skin`,
      {
        method: "POST",
        headers: createHeaders(),
        body: JSON.stringify(dataWithSubject),
      }
    );

    return handleResponse(analyzeResponse);
  },

  // Routines endpoints
  async getRoutines() {
    const response = await fetch("/api/routines", {
      method: "GET",
      headers: createHeaders(),
    });

    return handleResponse(response);
  },

  async createRoutine(routineData) {
    const response = await fetch("/api/routines", {
      method: "POST",
      headers: createHeaders(),
      body: JSON.stringify(routineData),
    });

    return handleResponse(response);
  },

  async updateRoutine(routineId, routineData) {
    const response = await fetch(`/api/routines/${routineId}`, {
      method: "PUT",
      headers: createHeaders(),
      body: JSON.stringify(routineData),
    });

    return handleResponse(response);
  },
};

export default apiService;
