query "auth/totp/enable" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text code filters=trim
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

    precondition (($input.code|strlen) == 6) {
      error_type = "inputerror"
      error = "Informe um código TOTP de 6 dígitos."
    }
  }

  response = {enabled: true}
  guid = "y8HJBgT7xfZWtwC1rC2pzJNClLw"
}
