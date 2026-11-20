query "appointments/{id}/reschedule" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int id
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
      error = "Apenas clientes ativos podem remarcar agendamentos."
    }

    db.get "appointment" {
      field_name = "id"
      field_value = $input.id
    } as $appointment

    precondition ($appointment != null && $appointment.client_id == $actor.id) {
      error_type = "accessdenied"
      error = "Você não tem acesso a este agendamento."
    }

    precondition ($appointment.status == "pending" || $appointment.status == "confirmed") {
      error_type = "badrequest"
      error = "Este agendamento não pode ser remarcado."
    }

    precondition ($appointment.start_time >= now|add_secs_to_timestamp:43200) {
      error_type = "badrequest"
      error = "A remarcação deve ser feita com pelo menos 12 horas de antecedência."
    }

    db.transaction {
      stack {
        db.add_or_edit "barber_booking_lock" {
          field_name = "barber_id"
          field_value = $appointment.barber_id
          data = {
            barber_id : $appointment.barber_id
            updated_at: now
          }
        } as $booking_lock

        db.get "service" {
          field_name = "id"
          field_value = $appointment.service_id
        } as $service

        var $end_time {
          value = $input.start_time|add_secs_to_timestamp:($appointment.duration_minutes_snapshot * 60)
        }

        var $requested_busy_end {
          value = $input.start_time|add_secs_to_timestamp:(($appointment.duration_minutes_snapshot * 60) + 900)
        }

        var $local_date {
          value = $input.start_time|format_timestamp:"Y-m-d":"America/Sao_Paulo"
        }

        var $opening {
          value = ($local_date ~ " 09:00:00")|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
        }

        var $closing {
          value = ($local_date ~ " 18:00:00")|parse_timestamp:"Y-m-d H:i:s":"America/Sao_Paulo"
        }

        var $weekday {
          value = $input.start_time|format_timestamp:"N":"America/Sao_Paulo"
        }

        var $earliest {
          value = now|add_secs_to_timestamp:7200
        }

        var $latest {
          value = now|add_secs_to_timestamp:2592000
        }

        precondition ($input.start_time >= $earliest && $input.start_time <= $latest && $weekday != "7" && $input.start_time >= $opening && $requested_busy_end <= $closing) {
          error_type = "badrequest"
          error = "O novo horário está fora do expediente ou do período permitido."
        }

        db.query "appointment" {
          where = $db.appointment.barber_id == $appointment.barber_id && $db.appointment.id != $appointment.id && $db.appointment.start_time < $requested_busy_end && $db.appointment.end_time > $opening && $db.appointment.status != "cancelled"
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

        var $old_start {
          value = $appointment.start_time
        }

        var $old_end {
          value = $appointment.end_time
        }

        db.edit "appointment" {
          field_name = "id"
          field_value = $appointment.id
          data = {
            start_time: $input.start_time
            end_time  : $end_time
            updated_at: now
          }
        } as $rescheduled

        db.add "appointment_status_history" {
          data = {
            appointment_id: $appointment.id
            from_status   : $appointment.status
            to_status     : $appointment.status
            changed_by    : $actor.id
            changed_at    : now
            notes         : "Remarcado de " ~ ($old_start|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo") ~ " para " ~ ($input.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo")
          }
        } as $history

        db.add "reschedule_history" {
          data = {
            appointment_id: $appointment.id
            changed_by    : $actor.id
            changed_at    : now
            old_start_time: $old_start
            new_start_time: $input.start_time
          }
        } as $audit
      }
    }
  }

  response = {
    id                       : $rescheduled.id
    client_id                : $rescheduled.client_id
    barber_id                : $rescheduled.barber_id
    service_id               : $rescheduled.service_id
    service_title_snapshot   : $rescheduled.service_title_snapshot
    price_snapshot           : $rescheduled.price_snapshot
    duration_minutes_snapshot: $rescheduled.duration_minutes_snapshot
    start_time               : $rescheduled.start_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    end_time                 : $rescheduled.end_time|format_timestamp:"Y-m-d\\TH:i:sP":"America/Sao_Paulo"
    status                   : $rescheduled.status
  }
}
