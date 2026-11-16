// Get the user record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = ""

  input {
  }

  stack {
    // Get the user record based on the auth ID
    db.get "" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "phone", "role", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "get_auth_user"
      }
    } as $event_log
  }

  response = {
    id   : $user.id
    name : $user.name
    email: $user.email
    phone: $user.phone
    role : $user.role
  }
  tags = ["xano:quick-start"]
  guid = "gZw_eUnPtJJCXRh8vh7oixOejtw"
}