query "auth/password-reset" verb=POST {
  api_group = "Authentication"

  input {
    email email filters=trim|lower
  }

  stack {
    function.run "Quick Start/generate_magic_link" {
      input = {email: $input.email}
    } as $reset_link

    conditional {
      if ($reset_link.token != "") {
        var $magic_link {
          value = $env.APP_BASE_URL ~ "/recuperar-senha?email=" ~ ($reset_link.email|url_encode) ~ "&token=" ~ ($reset_link.token|url_encode)
        }

        util.template_engine {
          value = """
            <p>Recebemos um pedido para redefinir sua senha.</p>
            <p><a href="{{ $var.magic_link }}">Criar uma nova senha</a></p>
            <p>Se você não solicitou esta alteração, ignore esta mensagem.</p>
            """
        } as $message

        util.send_email {
          service_provider = "resend"
          api_key = $env.RESEND_API_KEY
          subject = "Redefinição de senha BarberFlow"
          message = $message
          to = $reset_link.email
          from = $env.RESEND_FROM_EMAIL
        } as $email_result
      }
    }
  }

  response = {
    message: "Se o e-mail estiver cadastrado, enviaremos um link para redefinir sua senha."
  }
}
