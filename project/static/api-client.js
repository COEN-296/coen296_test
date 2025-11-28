// API Configuration
const API_BASE = window.location.origin;

// API client for reimbursement requests
const API = {
    // Get all requests
    async getAllRequests() {
        const response = await fetch(`${API_BASE}/api/requests`);
        return await response.json();
    },

    // Get requests by email
    async getRequestsByEmail(email) {
        const response = await fetch(`${API_BASE}/api/requests/email/${encodeURIComponent(email)}`);
        return await response.json();
    },

    // Get pending requests
    async getPendingRequests() {
        const response = await fetch(`${API_BASE}/api/requests/status/pending`);
        return await response.json();
    },

    // Create new request (supports FormData for file uploads)
    async createRequest(data) {
        // If data is FormData, don't set Content-Type header (browser sets it with boundary)
        const isFormData = data instanceof FormData;
        const headers = isFormData ? {} : { 'Content-Type': 'application/json' };
        const body = isFormData ? data : JSON.stringify(data);

        const response = await fetch(`${API_BASE}/api/requests`, {
            method: 'POST',
            headers: headers,
            body: body
        });
        return await response.json();
    },

    // Update request status
    async updateRequestStatus(requestId, status, reason = null) {
        const body = { status };
        if (reason) body.reason = reason;

        const response = await fetch(`${API_BASE}/api/requests/${requestId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return await response.json();
    },

    // Delete request
    async deleteRequest(requestId) {
        const response = await fetch(`${API_BASE}/api/requests/${requestId}`, {
            method: 'DELETE'
        });
        return await response.json();
    },

    // Get system logs
    async getLogs() {
        try {
            const response = await fetch(`${API_BASE}/logs`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching logs:', error);
            return [];
        }
    }
};
