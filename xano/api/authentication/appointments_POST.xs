query "appointments" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int barber_id
    int service_id
    int[] service_ids?
    timestamp start_time
  }

  stack {
    db.get "user" {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "role", "active"]
    } as $actor

    precondition ($actor != null && $actor.active == true && $actor.role == "client") {
      error_type = "accessdenied"
      error = "Apenas clientes ativos podem criar agendamentos."
    }

    db.get "barber" {
      field_name = "id"
      field_value = $input.barber_id
    } as $barber

    precondition ($barber != null && $barber.active == true) {
      error_type = "inputerror"
      error = "Selecione um serviço e barbeiro ativos."
    }

    db.get "user" {
      field_name = "id"
      field_value = $barber.user_id
      output = ["id", "role", "active"]
    } as $barber_user

    db.get "service" {
      field_name = "id"
      field_value = $input.service_id
    } as $service

    precondition ($barber_user != null && $barber_user.active == true && $barber_user.role == "barber" && $service != null && $service.active == true && $service.duration_minutes != null && $service.duration_minutes > 0) {
      error_type = "inputerror"
      error = "Selecione um serviço e barbeiro ativos."
    }

    var $combined_duration {
      value = $service.duration_minutes
    }
    var $combined_price {
      value = $service.price
    }
    var $combined_title {
      value = $service.title
    }

    conditional {
      if ($input.service_ids != null) {
        foreach ($input.service_ids) {
          each as $selected_service_id {
            conditional {
              if ($selected_service_id != $input.service_id) {
                db.get "service" {
                  field_name = "id"
                  field_value = $selected_service_id
                } as $selected_service

                precondition ($selected_service != null && $selected_service.active == true) {
                  error_type = "inputerror"
                  error = "Selecione somente serviços ativos."
                }

                var.update $combined_duration {
                  value = $combined_duration + $selected_service.duration_minutes
                }
                var.update $combined_price {
                  value = $combined_price + $selected_service.price
                }
                var.update $combined_title {
                  value = $combined_title ~ " + " ~ $selected_service.title
                }
              }
            }
          }
        }
      }
    }

    var $local_date {
      value = $input.start_time|format_timestamp:"Y-m-d":"America/Sao_Paulo"
    }

    var $day_start_text {
      value = $local_date ~ " 00:00:00"
    }

    var $opening_text {
      value = $local_date ~ " 09:00:00"
    }

    var $closing_text {
      value = $local_date ~ " 18:00:00"
    }

    var $day_start {
      value = $day_start_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $opening {
      value = $opening_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $closing {
      value = $closing_text|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
    }

    var $weekday {
      value = $day_start|format_timestamp:"N":"America/Sao_Paulo"
    }

    var $end_time {
      value = $input.start_time|add_secs_to_timestamp:($combined_duration * 60)
    }

    var $requested_busy_end {
      value = $input.start_time|add_secs_to_timestamp:(($combined_duration * 60) + 900)
    }

    var $earliest {
      value = now|add_secs_to_timestamp:7200
    }

    var $latest {
      value = now|add_secs_to_timestamp:2592000
    }

    precondition ($input.start_time >= $earliest && $input.start_time <= $latest && $weekday != "7" && $input.start_time >= $opening && $requested_busy_end <= $closing) {
      error_type = "inputerror"
      error = "O horário está fora do expediente ou do período permitido para agendamento."
    }

    db.transaction {
      stack {
        db.add_or_edit "barber_booking_lock" {
          field_name = "barber_id"
          field_value = $barber.id
          data = {
            barber_id : $barber.id
            updated_at: now
          }
        } as $booking_lock

        db.query "appointment" {
          where = $db.appointment.barber_id == $input.barber_id && $db.appointment.start_time < $requested_busy_end && $db.appointment.end_time > $day_start && $db.appointment.status != "cancelled"
          output = ["id", "start_time", "end_time"]
          return = {type: "list"}
        } as $busy

        var $has_conflict {
          value = false
        }

        foreach ($busy) {
          each as $existing {
            var $busy_end {
              value = $existing.end_time|add_secs_to_timestamp:900
            }

            conditional {
              if ($existing.start_time < $requested_busy_end && $busy_end > $input.start_time) {
                var.update $has_conflict {
                  value = true
                }
              }
            }
          }
        }

        precondition ($has_conflict == false) {
          error_type = "badrequest"
          error = "appointment_conflict: Este horário não está mais disponível."
        }

        db.add "appointment" {
          data = {
            client_id                : $actor.id
            barber_id                : $barber.id
            service_id               : $service.id
            service_title_snapshot   : $combined_title
            price_snapshot           : $combined_price
            duration_minutes_snapshot: $combined_duration
            start_time               : $input.start_time
            end_time                 : $end_time
            status                   : "pending"
            updated_at               : "now"
          }
        } as $appointment

        db.add "appointment_status_history" {
          data = {
            appointment_id: $appointment.id
            from_status   : null
            to_status     : "pending"
            changed_by    : $actor.id
            changed_at    : "now"
            notes         : "Agendamento criado"
          }
        } as $history
      }
    }
  }

  response = {
    id                       : $appointment.id
    client_id                : $appointment.client_id
    barber_id                : $appointment.barber_id
    service_id               : $appointment.service_id
    service_title_snapshot   : $combined_title
    price_snapshot           : $combined_price
    duration_minutes_snapshot: $combined_duration
    start_time               : $appointment.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    end_time                 : $appointment.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    status                   : "pending"
  }
  guid = "ZFmQbsIetu5IQXx7aL8wk6Etm5w"
}
