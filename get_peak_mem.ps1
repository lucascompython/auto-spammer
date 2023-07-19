param (
    [Parameter(Mandatory = $true)][string]$proc_name
)

$proc = Start-Process -PassThru -FilePath $proc_name

$mem = 0
# I hate Windows
do {
    $proc.Refresh()
    if ($proc.WorkingSet64 -gt $mem) {
        $mem = $proc.WorkingSet64
    }
} while (!$proc.WaitForExit(10))

Write-Output "$($mem)" 
