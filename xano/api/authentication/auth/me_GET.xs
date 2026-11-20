// Get the user record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    // Get the user record based on the auth ID
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "phone", "role", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    db.get "account_security" {
      field_name = "user_id"
      field_value = $user.id
    } as $security

  }

  response = {
    id   : $user.id
    name : $user.name
    email: $user.email
    phone: $user.phone
    role : $user.role
    avatar_url: $security != null ? $security.avatar_url : null
  }
  tags = ["xano:quick-start"]
  guid = "gZw_eUnPtJJCXRh8vh7oixOejtw"
}