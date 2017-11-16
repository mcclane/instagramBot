### Instagram Bot V2
Uses instagram private api, instead of a phantomjs

## requirements:
* python3
* pandas

## usage:
  ```shell  
  python3 controller.py
  ```

## Flags:

### Sample Invocation:

```shell
python3 controller.py  --hashtag_type=surfing --number_of_tags=20 --username hoopty --password floopty
```

###All arguments:
* hashtag_type : grouping of hashtags to randomly visit posts from
* delay : time (rough) between each bot action
* pipe_depth : maximum number of account should follow
* number_of_tags : number of hashtags bot will exhaustively visit
* cycle: follow number of users passed in, then unfollow them all
* username: username, if not passed in ask for user input
* password: password, if not passed in ask for user input
