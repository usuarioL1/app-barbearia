query "appointments/{id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true) {
      error_type = "unauthorized"
      error = "Sessão inválida ou expirada."
    }

    db.get "appointment" {
      field_name = "id"
      field_value = $input.id
    } as $appointment

    precondition ($appointment != null) {
      error_type = "notfound"
      error = "Agendamento não encontrado."
    }

    var $authorized {
      value = $actor.role == "admin"
    }

    conditional {
      if ($actor.role == "client" && $appointment.client_id == $actor.id) {
        var.update $authorized {
          value = true
        }
      }
    }

    conditional {
      if ($actor.role == "barber") {
        db.get "barber" {
          field_name = "user_id"
          field_value = $actor.id
        } as $barber

        conditional {
          if ($barber != null && $appointment.barber_id == $barber.id) {
            var.update $authorized {
              value = true
            }
          }
        }
      }
    }

    precondition ($authorized == true) {
      error_type = "accessdenied"
      error = "Você não tem acesso a este agendamento."
    }

    db.get "user" {
      field_name = "id"
      field_value = $appointment.client_id
      output = ["id", "name"]
    } as $client

    db.get "barber" {
      field_name = "id"
      field_value = $appointment.barber_id
    } as $barber_record

    db.get "user" {
      field_name = "id"
      field_value = $barber_record.user_id
      output = ["id", "name"]
    } as $barber_user

    var $status {
      value = $appointment.status
    }

    conditional {
      if ($status == null) {
        var.update $status {
          value = "pending"
        }
      }
    }
  }

  response = {
    id                       : $appointment.id
    client_id                : $appointment.client_id
    client_name              : $client.name
    barber_id                : $appointment.barber_id
    barber_name              : $barber_user.name
    service_id               : $appointment.service_id
    service_title_snapshot   : $appointment.service_title_snapshot
    price_snapshot           : $appointment.price_snapshot
    duration_minutes_snapshot: $appointment.duration_minutes_snapshot
    start_time               : $appointment.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    end_time                 : $appointment.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    status                   : $status
  }
  guid = "bBEbsc6yWiE8TPdT-XPNKJ55RFw"
}
