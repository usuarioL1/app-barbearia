table "password_reset" {
  auth = false
  schema {
    int id
    int user_id {
      table = "user"
    }
    password token_hash
    timestamp expires_at
    bool used?=false
    timestamp created_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "user_id"}]}
  ]
}
