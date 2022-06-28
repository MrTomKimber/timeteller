# timeteller

This is a small demo showing how an svg image can be generated in code.

In this instance the images show clock faces (both analogue and digital) that reflect the current time.

A flask server dishes up the page according to a simple API.

Run the flask server using the ```go_tt.sh``` command, you may need to edit this for a windows machine into a batch-equivalent.

An empty URL suffix will signal the server to display the current time (refresh the page to update)

```
/show/<time>/
```

where ```<time>``` is HH:MM

Will display the time specified
