table "barber" {
  auth = false
  schema {
    int id
    int user_id {
      table = "user"
    }
    text specialty filters=trim
    text bio?
    bool active?=true
    timestamp created_at?=now
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "active"}]}
  ]
}
