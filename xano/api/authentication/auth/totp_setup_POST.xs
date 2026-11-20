query "auth/totp/setup" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    var $secret {
      value = (|uuid)|replace:"-":""|substr:0:32
    }

    db.add_or_edit "account_security" {
      field_name = "user_id"
      field_value = $user.id
      data = {
        user_id: $user.id
        pending_totp_secret: $secret
        totp_enabled: false
        session_version: 0
      }
    } as $security
  }

  response = {secret: $secret}
  guid = "uEa3E6rtxYhCPoOLj24hmOe6Gg8"
}
