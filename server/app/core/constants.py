# Authentication Logs
AUTH_LOGIN_ATTEMPT = "Login attempt for user: {username}"
AUTH_LOGIN_SUCCESS = "User {username} logged in successfully"
AUTH_LOGIN_FAILED = "Invalid credentials for user: {username}"
AUTH_REFRESH_ATTEMPT = "Refresh token attempt for user: {username}"
AUTH_REFRESH_SUCCESS = "New access token issued for user: {username}"
AUTH_REFRESH_FAILED = "Refresh token invalid or expired for user: {username}"

# User Management Logs
USER_CREATE = "New user created: {username}"
USER_UPDATE = "User updated: {username}"
USER_DELETE = "User deleted: {username}"

# Database Logs
DB_CONNECTION_SUCCESS = "Database connection established successfully"
DB_CONNECTION_FAILED = "Database connection failed: {error}"
DB_QUERY_EXECUTION = "Executing DB query: {query}"

# Security Logs
SEC_TOKEN_DECODE_SUCCESS = "Token decoded successfully for subject: {subject}"
SEC_TOKEN_DECODE_FAILED = "Failed to decode token: {error}"
SEC_PASSWORD_HASH = "Password hashed for user: {username}"
SEC_PASSWORD_VERIFY_SUCCESS = "Password verified successfully for user: {username}"
SEC_PASSWORD_VERIFY_FAILED = "Password verification failed for user: {username}"
