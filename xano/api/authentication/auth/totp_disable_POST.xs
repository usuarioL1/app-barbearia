query "auth/totp/disable" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text current_password
    text code
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "password", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    security.check_password {
      text_password = $input.current_password
      hash_password = $user.password
    } as $password_valid

    precondition ($password_valid) {
      error_type = "unauthorized"
      error = "Credenciais inválidas."
    }

    db.edit "account_security" {
      field_name = "user_id"
      field_value = $user.id
      data = {
        totp_enabled: false
        totp_secret: null
        pending_totp_secret: null
      }
    } as $updated
  }

  response = {enabled: false}
  guid = "YzVtrTDUjyuneTfEUNYZCUawW34"
}
