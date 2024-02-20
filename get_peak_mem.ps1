param (
    [Parameter(Mandatory = $true)][string]$proc_name
)

$proc = Start-Process -PassThru -FilePath $proc_name

$mem = 0
# I hate Windows
do {
    $proc.Refresh()
    if ($proc.PeakWorkingSet64 -gt $mem) {
        $mem = $proc.PeakWorkingSet64
    }
} while (!$proc.WaitForExit(10))

Write-Output "$($mem)" 

