function "enforce_session_version" {
  input {
    int user_id
    int token_session_version?
  }

  stack {
    db.get "account_security" {
      field_name = "user_id"
      field_value = $input.user_id
    } as $security

    var $current_version {
      value = $security != null ? $security.session_version : 0
    }

    var $claimed_version {
      value = $input.token_session_version != null ? $input.token_session_version : 0
    }

    precondition ($claimed_version == $current_version) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }
  }

  response = $current_version
  guid = "qLb8-wfHS5f5ElaCed-rT9mf2JU"
}
