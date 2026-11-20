query "auth/me" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text name filters=trim
    email email filters=trim|lower
    text phone filters=trim
    text avatar_url? filters=trim
  }

  stack {
    precondition (($input.name|strlen) > 0 && ($input.phone|strlen) >= 10) {
      error_type = "inputerror"
      error = "Informe nome e telefone válidos."
    }

    conditional {
      if ($input.avatar_url != null && $input.avatar_url != "") {
        precondition (($input.avatar_url|starts_with:"https://") && ($input.avatar_url|strlen) <= 2048) {
          error_type = "inputerror"
          error = "Informe uma URL HTTPS válida."
        }
      }
    }

    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "active"]
    } as $user

    precondition ($user != null && $user.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    db.get "user" {
      field_name = "email"
      field_value = $input.email
      output = ["id"]
    } as $email_owner

    precondition ($email_owner == null || $email_owner.id == $auth.id) {
      error_type = "accessdenied"
      error = "Este e-mail já está em uso."
    }

    db.edit "user" {
      field_name = "id"
      field_value = $auth.id
      data = {
        name : $input.name
        email: $input.email
        phone: $input.phone
      }
    } as $updated_user

    db.add_or_edit "account_security" {
      field_name = "user_id"
      field_value = $auth.id
      data = {
        user_id        : $auth.id
        avatar_url     : $input.avatar_url
        session_version: 0
        totp_enabled   : false
      }
    } as $security

    function.run "Quick Start/log_event" {
      input = {user_id: $auth.id, action: "profile_updated"}
    } as $event_log
  }

  response = {
    id   : $updated_user.id
    name : $updated_user.name
    email: $updated_user.email
    phone: $updated_user.phone
    role : $updated_user.role
    avatar_url: $security.avatar_url
  }
  guid = "S_cFHTuV75aOhCCagpGAtJd9P2c"
}
