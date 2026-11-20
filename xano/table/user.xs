table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email email filters=trim|lower
    password password
    text phone filters=trim
    enum role?=client {
      values = ["client", "barber", "admin"]
    }
    bool active?=true
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email"}]}
    {type: "btree", field: [{name: "role"}]}
    {type: "btree", field: [{name: "active"}]}
  ]

  guid = "ICs5B10_99DF4n2YF1PrB17uqT8"
}
