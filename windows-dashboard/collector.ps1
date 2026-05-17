$db = "dashboard.db"

sqlite3 $db "CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    source TEXT,
    level TEXT,
    alert TEXT,
    message TEXT
);"

$logsToRead = @(
    "Security",
    "System",
    "Application",
    "Microsoft-Windows-Windows Firewall With Advanced Security/Firewall"
)

$lastTime = (Get-Date).AddMinutes(-5)

while ($true) {

    foreach ($logName in $logsToRead) {

        $events = Get-WinEvent -FilterHashtable @{
            LogName   = $logName
            StartTime = $lastTime
        } -ErrorAction SilentlyContinue

        foreach ($event in $events) {

            $level = "INFO"
            $alert = "NORMAL"

            if ($event.Id -eq 4625) {
                $level = "CRITICAL"
                $alert = "FAILED_LOGIN"
            }
            elseif ($event.Id -eq 4624) {
                $level = "INFO"
                $alert = "SUCCESS_LOGIN"
            }
            elseif ($event.Id -eq 4720) {
                $level = "WARNING"
                $alert = "USER_CREATED"
            }
            elseif ($event.Id -eq 4726) {
                $level = "CRITICAL"
                $alert = "USER_DELETED"
            }
            elseif ($event.Id -eq 1102) {
                $level = "CRITICAL"
                $alert = "SECURITY_LOG_CLEARED"
            }
            elseif ($event.Id -eq 7045) {
                $level = "WARNING"
                $alert = "SERVICE_INSTALLED"
            }
            elseif ($logName -like "*Firewall*") {
                $level = "WARNING"
                $alert = "FIREWALL_EVENT"
            }
            elseif ($event.Level -eq 1 -or $event.Level -eq 2) {
                $level = "CRITICAL"
                $alert = "CRITICAL_EVENT"
            }
            elseif ($event.Level -eq 3) {
                $level = "WARNING"
                $alert = "WARNING_EVENT"
            }
            

            $time = $event.TimeCreated.ToString("dd/MM/yyyy HH:mm:ss")
            $source = $event.ProviderName
            $msg = $event.Message

            if ($null -eq $msg) {
                $msg = ""
            }

            $msg = $msg.Replace("'", " ")
            $source = $source.Replace("'", " ")

            sqlite3 $db "INSERT INTO logs (time, source, level, alert, message)
            VALUES ('$time', '$source', '$level', '$alert', '$msg');"

            Write-Host "[$level] [$alert] $time - $source - $msg"
        }
    }

    $lastTime = Get-Date
    Start-Sleep -Seconds 5
}