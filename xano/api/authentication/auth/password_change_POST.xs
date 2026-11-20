query "auth/password/change" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text current_password
    text new_password
    text totp_code?
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

    precondition (($input.new_password|strlen) >= 8) {
      error_type = "inputerror"
      error = "A nova senha deve conter pelo menos 8 caracteres."
    }

    security.check_password {
      text_password = $input.current_password
      hash_password = $user.password
    } as $password_valid

    precondition ($password_valid) {
      error_type = "unauthorized"
      error = "Credenciais inválidas."
    }

    db.edit "user" {
      field_name = "id"
      field_value = $user.id
      data = {password: $input.new_password}
    } as $updated
  }

  response = {changed: true}
  guid = "KjoRf5P1F83ojy5gicsk7nqSmWw"
}
