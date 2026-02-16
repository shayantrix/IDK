# IDK
I really dont know what I am doing here but lets go forward and see

#### mongodb replicas
```docker exec -it mongodb1 mongosh --port 30001```

> inside the shell
  ```
    rs.initiate({
      _id: "my-replica-set",
      members: [
        { _id: 0, host: "mongodb1:30001" },
        { _id: 1, host: "mongodb2:30002" },
        { _id: 2, host: "mongodb3:30003" }
      ]
    })
  
    rs.status()
  
  ```
