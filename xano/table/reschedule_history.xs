table "reschedule_history" {
  auth = false
  schema {
    int id
    int appointment_id {
      table = "appointment"
    }
    int changed_by {
      table = "user"
    }
    timestamp changed_at?=now
    timestamp old_start_time
    timestamp new_start_time
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "appointment_id"}, {name: "changed_at"}]}
  ]
  guid = "LS2j14uHbUuTtfMT0Q9qnpEiXTY"
}
