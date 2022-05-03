# project1_back-end

## 플라스크(python)
```
· RestFul api
· server : AWS EC2 with docker
· database : 
    - local(test-server) AWS EC2 width docker(mysql)
    - server AWS RDS mysql
```

## 주요 라이브러리
```
· swagger : flasgger
· mysql : mysql.connector
· token : pyjwt
```

## 빌드
```
· install : docker-compose up -d
· update : 
    - docker-compose pull
      docker-compose up --force-recreate --build -d
      docker image prune -f
```
      