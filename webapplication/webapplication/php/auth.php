<?php


// File: webapplication/php/auth.php

require __DIR__ . '/config_redis.php'; // for getRedis()

function getUserIdFromSession(?string $session): ?int {

  if (!$session) return null;
  $redis = getRedis();


  //key must same as saved it in login.php: "sess:<sessionId>" => <userId>
  
  $uid = $redis->get("sess:$session");
  return $uid !== false ? (int)$uid : null;


}
