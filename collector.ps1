$db = "dashboard.db"

$logsToRead = @(
    "System",
    "Application",
    "Security"
)

$lastTime = (Get-Date).AddMinutes(-5)

while ($true) {
    foreach ($logName in $logsToRead) {
        $events = Get-WinEvent -FilterHashtable @{
            LogName = $logName
            StartTime = $lastTime
        } -ErrorAction SilentlyContinue

        foreach ($event in $events) {
            $level = "INFO"

            if ($event.Level -eq 1) {
                $level = "CRITICAL"
            }
            elseif ($event.Level -eq 2) {
                $level = "CRITICAL"
            }
            elseif ($event.Level -eq 3) {
                $level = "WARNING"
            }

            $time = $event.TimeCreated.ToString("dd/MM/yyyy HH:mm:ss")
            $source = $event.ProviderName
            $msg = $event.Message

            if ($null -eq $msg) {
                $msg = ""
            }

            $msg = $msg.Replace("'", " ")

            sqlite3 $db "INSERT INTO logs (time, source, level, message) VALUES ('$time', '$source', '$level', '$msg');"

            Write-Host "[$level] $time - $source - $msg"
        }
    }

    $lastTime = Get-Date
    Start-Sleep -Seconds 5
}