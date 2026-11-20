table "barber_booking_lock" {
  auth = false

  schema {
    int id
    int barber_id {
      table = "barber"
    }
    timestamp updated_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "barber_id"}]}
  ]

  guid = "gCS2j1Uvf6gQukz4DQXBtphmOyA"
}
