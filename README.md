# IDK
I really dont know what I am doing here but lets go forward and see
Building AI-agent which is works by the documents I feed it. In my own example I tried to make a really clever system that can handle System networking better than anyone :D, well not better than humans with 20 years of job experience I wish :). But really you can feed it the url of the book (.pdf) that you want it to be expert in and answer your questions.
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
