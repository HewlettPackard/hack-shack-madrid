Import-Module HPOneView.410

Connect-HPOVMgmt -Hostname 192.168.2.50 -UserName Administrator -Password password

foreach ($profile in Get-HPOVServerProfile) {
    $profile.connections | % {
        if ($_.mac -eq 'F2:65:D6:40:00:08') {
            Write-Output "Found MAC in profile " $profile.name
        }
    }
}

Disconnect-HPOVMgmt
