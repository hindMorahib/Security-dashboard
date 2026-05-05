$db = "dashboard.db"

# créer la base + table si elle n'existe pas
sqlite3 $db "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT, message TEXT);"

while ($true) {
    $events = Get-WinEvent -LogName System -MaxEvents 10

    foreach ($event in $events) {
        $level = "INFO"

        if ($event.LevelDisplayName -eq "Error") {
            $level = "CRITICAL"
        }
        elseif ($event.LevelDisplayName -eq "Warning") {
            $level = "WARNING"
        }

        $message = $event.TimeCreated.ToString() + " - " + $event.ProviderName + " - " + $event.Message.Replace("'", " ")

        sqlite3 $db "INSERT INTO logs (level, message) VALUES ('$level', '$message');"

        Write-Host "[$level] $message"
    }

    Start-Sleep -Seconds 5
}