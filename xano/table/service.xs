table "service" {
  auth = false
  schema {
    int id
    text title filters=trim
    text description?
    decimal price filters=min:0.01
    int duration_minutes filters=min:1
    bool active?=true
    timestamp created_at?=now
    timestamp updated_at?=now
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "active"}]}
  ]

  items = [
    {
      id              : 4
      title           : "Sobrancelha"
      description     : "Design de sobrancelhas"
      price           : "20.00000"
      duration_minutes: 15
      active          : true
      created_at      : 1795180324429
      updated_at      : 1795180324429
    }
    {
      id              : 5
      title           : "Pezinho / Acabamento"
      description     : "Acabamento de contorno e costeletas"
      price           : "15.00000"
      duration_minutes: 15
      active          : true
      created_at      : 1795180324429
      updated_at      : 1795180324429
    }
    {
      id              : 6
      title           : "Hidratação Capilar"
      description     : "Tratamento hidratante para os fios"
      price           : "40.00000"
      duration_minutes: 30
      active          : true
      created_at      : 1795180324429
      updated_at      : 1795180324429
    }
  ]
  guid = "urb4NYLWFvUXXnlQZimUF3cUnK8"
}
