# spyder

Spy and spider !

## Config.yml

```
-
  url: somesite.com
  get: pathfoo/*
-
  url: other.com
  get: pathcrazy/and/much/crazy/*

```

Goes only 1 lvl , saves to:

```
  somesite.com/id1/data.txt
  somesite.com/id1/data.jpg/jpeg/png/webp/avif

  other.com/pathcrazyandmuchcrazy/data.txt
  other.com/pathcrazyandmuchcrazy/media.jpg/jpeg/png/webp/avif
```

## Use


    ./spyder all
    ./spyder somesite
