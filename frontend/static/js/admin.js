/**
 * FinSight – Admin JS
 * Loads users, toggle active status.
 */
document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    if (!Auth.isAdmin()) {
        showToast('Admin access required', 'error');
        setTimeout(() => window.location.href = '/pages/dashboard.html', 1000);
        return;
    }
    loadUsers();
});

async function loadUsers() {
    const tbody = document.getElementById('users-tbody');
    try {
        const users = await api.get('/admin/users');
        tbody.innerHTML = users.map(u => `
            <tr>
                <td>${u.id}</td>
                <td>${u.name}</td>
                <td>${u.email}</td>
                <td><span class="badge ${u.role === 'admin' ? 'badge-primary' : 'badge-info'}">${u.role}</span></td>
                <td>${u.is_email_verified ? '<span class="badge badge-success">Yes</span>' : '<span class="badge badge-warning">No</span>'}</td>
                <td>${u.is_active ? '<span class="badge badge-success">Active</span>' : '<span class="badge badge-danger">Disabled</span>'}</td>
                <td>${u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}</td>
                <td>
                    <button class="btn btn-sm ${u.is_active ? 'btn-danger' : 'btn-success'}"
                            onclick="toggleUser(${u.id})">
                        ${u.is_active ? 'Disable' : 'Enable'}
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="8" style="color:var(--danger)">Failed to load users</td></tr>';
    }
}

async function toggleUser(userId) {
    try {
        await api.put(`/admin/users/${userId}/toggle`);
        showToast('User status updated', 'success');
        loadUsers();
    } catch (e) {
        showToast(e.error || 'Failed to update', 'error');
    }
}
