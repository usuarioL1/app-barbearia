query "auth/password-reset/confirm" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
    text token filters=trim
    text password
  }

  stack {
    precondition (($input.password|strlen) >= 8) {
      error_type = "inputerror"
      error = "A senha deve conter pelo menos 8 caracteres."
    }

    db.get "user" {
      field_name = "email"
      field_value = $input.email
      output = ["id", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "O link de redefinição é inválido ou expirou."
    }

    db.get "password_reset" {
      field_name = "user_id"
      field_value = $user.id
      output = ["id", "user_id", "token_hash", "expires_at", "used"]
    } as $reset

    precondition ($reset != null && $reset.used == false && $reset.expires_at > now) {
      error_type = "unauthorized"
      error = "O link de redefinição é inválido ou expirou."
    }

    security.check_password {
      text_password = $input.token
      hash_password = $reset.token_hash
    } as $token_matches

    precondition ($token_matches) {
      error_type = "unauthorized"
      error = "O link de redefinição é inválido ou expirou."
    }

    db.transaction {
      stack {
        db.edit "user" {
          field_name = "id"
          field_value = $user.id
          data = {password: $input.password}
        } as $updated_user

        db.edit "password_reset" {
          field_name = "id"
          field_value = $reset.id
          data = {used: true}
        } as $used_reset

        function.run "Quick Start/log_event" {
          input = {user_id: $user.id, action: "password_reset"}
        } as $event_log
      }
    }
  }

  response = {message: "Senha atualizada. Entre novamente."}
}
