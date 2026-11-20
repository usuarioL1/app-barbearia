query "admin/appointments" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    text from?
    text to?
    int barber_id?
    text status?
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && $actor.role == "admin") {
      error_type = "accessdenied"
      error = "Apenas administradores ativos podem consultar a agenda."
    }

    var $from_timestamp {
      value = null
    }

    var $to_timestamp {
      value = null
    }

    conditional {
      if ($input.from != null) {
        var $from_text {
          value = $input.from ~ " 00:00:00"
        }

        var.update $from_timestamp {
          value = $from_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
        }
      }
    }

    conditional {
      if ($input.to != null) {
        var $to_text {
          value = $input.to ~ " 00:00:00"
        }

        var.update $to_timestamp {
          value = $to_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"|add_secs_to_timestamp:86400
        }
      }
    }

    db.query "appointment" {
      join = {
        client: {table: "user", where: $db.appointment.client_id == $db.client.id}
        barber: {table: "barber", where: $db.appointment.barber_id == $db.barber.id}
        barber_user: {table: "user", where: $db.barber.user_id == $db.barber_user.id}
      }
      where = $db.appointment.start_time >=? $from_timestamp && $db.appointment.start_time <? $to_timestamp && $db.appointment.barber_id ==? $input.barber_id && $db.appointment.status ==? $input.status
      sort = {start_time: "asc"}
      eval = {
        client_name: $db.client.name
        barber_name: $db.barber_user.name
      }
      output = ["id", "client_id", "barber_id", "service_id", "service_title_snapshot", "price_snapshot", "duration_minutes_snapshot", "start_time", "end_time", "status"]
      return = {type: "list"}
    } as $appointments

    var $items {
      value = []
    }

    foreach ($appointments) {
      each as $appointment {
        var $item {
          value = {
            id                       : $appointment.id
            client_id                : $appointment.client_id
            client_name              : $appointment.client_name
            barber_id                : $appointment.barber_id
            barber_name              : $appointment.barber_name
            service_id               : $appointment.service_id
            service_title_snapshot   : $appointment.service_title_snapshot
            price_snapshot           : $appointment.price_snapshot
            duration_minutes_snapshot: $appointment.duration_minutes_snapshot
            start_time               : $appointment.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            end_time                 : $appointment.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
            status                   : $appointment.status
          }
        }

        var.update $items {
          value = $items|push:$item
        }
      }
    }
  }

  response = {items: $items}
  guid = "E_dFSuWzGHeAwQy82GLXRGCXLSQ"
}
