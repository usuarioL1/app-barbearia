query "auth/sessions/revoke-all" verb=POST {
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

    db.get "account_security" {
      field_name = "user_id"
      field_value = $user.id
    } as $security

    var $next_version {
      value = ($security != null ? $security.session_version : 0) + 1
    }

    db.add_or_edit "account_security" {
      field_name = "user_id"
      field_value = $user.id
      data = {
        user_id: $user.id
        session_version: $next_version
        totp_enabled: $security != null ? $security.totp_enabled : false
      }
    } as $updated
  }

  response = {revoked: true}
  guid = "lc-ObmiZHJId2ScVpc2apxDJ8S0"
}
