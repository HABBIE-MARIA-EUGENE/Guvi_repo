<?php
header('Content-Type: application/json');

const DEBUG = false;  // since it is wrkng

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  http_response_code(405);
  echo json_encode(['status'=>'error','message'=>'Method not allowed']);
  exit;
}

require __DIR__ . '/db.php';

$email = trim($_POST['email'] ?? '');
$pwd   = $_POST['password'] ?? '';

//vald. check

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
  echo json_encode(['status'=>'error','message'=>'Invalid email']);
  exit;
}
if (strlen($pwd) < 8) {
  echo json_encode(['status'=>'error','message'=>'Password must be ≥ 8 chars']);
  exit;
}

try {
  // duplicate check
  $q = $pdo->prepare("SELECT 1 FROM users WHERE email = ?");
  $q->execute([$email]);
  if ($q->fetch()) {
    echo json_encode(['status'=>'error','message'=>'Email already exists']);
    exit;
  }

  // must hash the pw always
  $hash = password_hash($pwd, PASSWORD_DEFAULT);

  // IMPORTANT:
  $ins = $pdo->prepare("INSERT INTO users (email, password) VALUES (?, ?)");
  $ins->execute([$email, $hash]);

  echo json_encode(['status'=>'ok','message'=>'Registered successfully']);
} catch (Throwable $e) {
  http_response_code(500);
  echo json_encode([
    'status'=>'error',
    'message'=> DEBUG ? $e->getMessage() : 'Server Error'
  ]);
}
