query "barber/appointments" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    text date
    text status?
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && $actor.role == "barber") {
      error_type = "accessdenied"
      error = "Apenas barbeiros ativos podem consultar sua agenda."
    }

    db.get "barber" {
      field_name = "user_id"
      field_value = $actor.id
    } as $barber

    precondition ($barber != null && $barber.active == true) {
      error_type = "accessdenied"
      error = "Perfil de barbeiro inativo."
    }

    var $day_start_text {
      value = $input.date ~ " 00:00:00"
    }

    var $next_day_text {
      value = $input.date ~ " 00:00:00"
    }

    var $day_start {
      value = $day_start_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $next_day_start {
      value = $next_day_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"|add_secs_to_timestamp:86400
    }

    db.query "appointment" {
      join = {
        client: {table: "user", where: $db.appointment.client_id == $db.client.id}
      }
      where = $db.appointment.barber_id == $barber.id && $db.appointment.start_time >= $day_start && $db.appointment.start_time < $next_day_start && $db.appointment.status ==? $input.status
      sort = {start_time: "asc"}
      eval = {
        client_name: $db.client.name
      }
      output = ["id", "client_id", "barber_id", "service_id", "service_title_snapshot", "price_snapshot", "duration_minutes_snapshot", "start_time", "end_time", "status"]
      return = {type: "list"}
    } as $appointments

    var $items {
      value = []
    }

    foreach ($appointments) {
      each as $appointment {
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

        var $item {
          value = {
            id                       : $appointment.id
            client_id                : $appointment.client_id
            client_name              : $appointment.client_name
            barber_id                : $appointment.barber_id
            service_id               : $appointment.service_id
            service_title_snapshot   : $appointment.service_title_snapshot
            price_snapshot           : $appointment.price_snapshot
            duration_minutes_snapshot: $appointment.duration_minutes_snapshot
            start_time               : $appointment.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            end_time                 : $appointment.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            status                   : $status
          }
        }

        var.update $items {
          value = $items|push:$item
        }
      }
    }
  }

  response = {items: $items}
  guid = "Ifowule7V6-HirZ_lHV-R63i_as"
}
